from sqlalchemy import text


async def create_table(engine):
    async with engine.begin() as conn:
        # Выполнение SQL-скрипта для создания таблицы
        create_table_sql = """
        create table if not exists public.sku
        (
            uuid                   uuid,
            marketplace_id         integer,
            product_id             bigint,
            title                  text,
            description            text,
            brand                  text,
            seller_id              integer,
            seller_name            text,
            first_image_url        text,
            category_id            integer,
            category_lvl_1         text,
            category_lvl_2         text,
            category_lvl_3         text,
            category_remaining     text,
            features               json,
            rating_count           integer,
            rating_value           double precision,
            price_before_discounts real,
            discount               double precision,
            price_after_discounts  real,
            bonuses                integer,
            sales                  integer,
            inserted_at            timestamp default now(),
            updated_at             timestamp default now(),
            currency               text,
            barcode                text,
            similar_sku            uuid[]
        );
        """
        await conn.execute(text(create_table_sql))
