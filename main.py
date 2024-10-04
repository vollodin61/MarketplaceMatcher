import asyncio

from environs import Env
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.es_utils import init_es
from app.models import Base
from app.parser import build_category_hierarchy, parse_xml


async def drop_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
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
    ELASTICSEARCH_URL = env("ELASTICSEARCH_HOST")
    ELASTICSEARCH_USER = env("ELASTICSEARCH_USER")
    ELASTICSEARCH_PASSWORD = env("ELASTICSEARCH_PASSWORD")

    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Пересоздаём таблицы
    await drop_tables(engine)
    await create_tables(engine)

    # Инициализируем Elasticsearch клиент
    es_client = await init_es(ELASTICSEARCH_URL, ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)

    # Сначала получаем категории
    categories, parent_map = build_category_hierarchy(env("PATH_TO_FILE"))

    async with async_session() as session:
        # Парсим офферы
        async for sku in parse_xml(env("PATH_TO_FILE"), categories, parent_map):
            session.add(sku)
            # # Индексируем товар в Elasticsearch
            # await index_in_elasticsearch(es_client, sku)
            #
            # # Находим похожие товары
            # similar_skus = await find_similar_skus(es_client, sku)
            #
            # # Обновляем поле similar_sku
            # sku.similar_sku = similar_skus

            await session.commit()

    await engine.dispose()
    await es_client.close()


if __name__ == "__main__":
    asyncio.run(main())
