import asyncio

from environs import Env
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.es_utils import find_similar_skus, index_in_elasticsearch, init_es
from app.models import Base
from app.parser import build_category_hierarchy, parse_xml


async def drop_tables(engine: AsyncEngine) -> None:
    """
    Удаляет все таблицы, определенные в базе данных, используя SQLAlchemy.

    Параметры:
    - engine: Асинхронный движок SQLAlchemy, используемый для выполнения операций с базой данных.

    Исключения:
    - Вызываются при ошибках соединения с базой данных или выполнения операций.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables(engine) -> None:
    """
    Создает все таблицы, определенные в базе данных, используя SQLAlchemy.

    Параметры:
    - engine: Асинхронный движок SQLAlchemy, используемый для выполнения операций с базой данных.

    Исключения:
    - Вызываются при ошибках соединения с базой данных или выполнения операций.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    """
    Основная асинхронная функция приложения, которая выполняет следующие действия:
    1. Читает переменные окружения из файла .env.
    2. Создает асинхронный движок для подключения к базе данных PostgreSQL.
    3. Удаляет и создает таблицы в базе данных.
    4. Инициализирует клиент Elasticsearch.
    5. Получает категории из XML файла и парсит офферы.
    6. Индексирует офферы в Elasticsearch и обновляет поле similar_sku.

    Исключения:
    - Вызываются при ошибках соединения с базой данных, выполнения операций или обработки данных.
    """
    env = Env()
    env.read_env()

    POSTGRES_HOST: str = env("POSTGRES_HOST")
    POSTGRES_PORT: str = env("POSTGRES_PORT")
    POSTGRES_USER: str = env("POSTGRES_USER")
    POSTGRES_PASSWORD: str = env("POSTGRES_PASSWORD")
    POSTGRES_DB: str = env("POSTGRES_DB")

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    ELASTICSEARCH_URL: str = env("ELASTICSEARCH_HOST")

    # Создание асинхронного движка SQLAlchemy
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Пересоздание таблиц
    await drop_tables(engine)
    await create_tables(engine)

    # Инициализация клиента Elasticsearch
    es_client = await init_es(ELASTICSEARCH_URL)

    # Получение категорий из XML файла
    categories, parent_map = build_category_hierarchy(env("PATH_TO_FILE"))

    async with async_session() as session:
        # Парсинг офферов
        async for sku in parse_xml(env("PATH_TO_FILE"), categories, parent_map):
            session.add(sku)
            # Индексирование товара в Elasticsearch
            await index_in_elasticsearch(es_client, sku)

            # Поиск похожих товаров
            similar_skus = await find_similar_skus(es_client, sku)

            # Обновление поля similar_sku
            sku.similar_sku = similar_skus
            print(f"{'_' * 29} Updating SKU {sku.uuid} with similar SKUs: {similar_skus}")  # Вывод информации

            await session.commit()

    # Закрытие соединения с базой данных и клиентом Elasticsearch
    await engine.dispose()
    await es_client.close()


if __name__ == "__main__":
    asyncio.run(main())
