from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def create_table(engine: AsyncEngine) -> None:
    """
    Создает таблицу 'sku' в базе данных, если она еще не существует.

    Параметры:
    - engine: Асинхронный движок SQLAlchemy, используемый для выполнения команд SQL.

    Исключения:
    - Вызываются при ошибках соединения с базой данных или выполнения SQL-запроса.
    """
    async with engine.begin() as conn:
        # Выполнение SQL-скрипта для создания таблицы
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS public.sku
        (
            uuid                   UUID PRIMARY KEY,
            marketplace_id         INTEGER,
            product_id             BIGINT,
            title                  TEXT,
            description            TEXT,
            brand                  TEXT,
            seller_id              INTEGER,
            seller_name            TEXT,
            first_image_url        TEXT,
            category_id            INTEGER,
            category_lvl_1         TEXT,
            category_lvl_2         TEXT,
            category_lvl_3         TEXT,
            category_remaining     TEXT,
            features               JSON,
            rating_count           INTEGER,
            rating_value           DOUBLE PRECISION,
            price_before_discounts REAL,
            discount               DOUBLE PRECISION,
            price_after_discounts  REAL,
            bonuses                INTEGER,
            sales                  INTEGER,
            inserted_at            TIMESTAMP DEFAULT NOW(),
            updated_at             TIMESTAMP DEFAULT NOW(),
            currency               TEXT,
            barcode                TEXT,
            similar_sku            UUID[]
        );
        """
        await conn.execute(text(create_table_sql))
