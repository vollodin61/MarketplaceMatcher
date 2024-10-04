import uuid
from datetime import datetime

from sqlalchemy import ARRAY, JSON, REAL, TIMESTAMP, BigInteger, Column, Double, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей, наследуется от AsyncAttrs и DeclarativeBase.
    Реализует поддержку асинхронных операций для SQLAlchemy моделей.
    """

    pass


class SKU(Base):
    """
    Модель для хранения информации о товаре (SKU - Stock Keeping Unit).
    Включает поля для информации о товаре, категории, характеристиках, рейтингах, ценах и прочих атрибутах.

    Поля:
    - uuid: Уникальный идентификатор товара в БД.
    - marketplace_id: ID маркетплейса, с которого получен товар.
    - product_id: ID товара в маркетплейсе.
    - title: Название товара.
    - description: Описание товара.
    - brand: Бренд товара.
    - seller_id: ID продавца.
    - seller_name: Имя продавца.
    - first_image_url: URL первой фотографии товара.
    - category_id: ID категории товара.
    - category_lvl_1, category_lvl_2, category_lvl_3: Разделы категории товара.
    - category_remaining: Остаток категорий товара.
    - features: Характеристики товара (JSON-формат).
    - rating_count: Количество отзывов на товар.
    - rating_value: Рейтинг товара (0-5).
    - price_before_discounts: Цена до скидок.
    - discount: Размер скидки.
    - price_after_discounts: Цена после скидок.
    - bonuses: Количество бонусов.
    - sales: Количество продаж.
    - inserted_at: Дата вставки записи.
    - updated_at: Дата обновления записи.
    - currency: Валюта товара.
    - barcode: Штрихкод товара.
    - similar_sku: Список UUID похожих товаров.
    """

    __tablename__ = "sku"

    # Поля таблицы SKU
    uuid: Mapped[PG_UUID] = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="id товара в нашей БД"
    )
    marketplace_id: Mapped[int] = mapped_column(nullable=False, comment="id маркетплейса")
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="id товара в маркетплейсе")
    title: Mapped[str] = mapped_column(comment="Название товара")
    description: Mapped[str] = mapped_column(comment="Описание товара")
    brand: Mapped[str] = mapped_column(index=True, comment="Бренд товара")
    seller_id: Mapped[int] = mapped_column(comment="ID продавца")
    seller_name: Mapped[str] = mapped_column(comment="Имя продавца")
    first_image_url: Mapped[str] = mapped_column(comment="URL первой фотографии товара")
    category_id: Mapped[int] = mapped_column(comment="ID категории товара")

    # Поля для категорий
    category_lvl_1: Mapped[str] = mapped_column(
        comment="Первая часть категории товара. "
        "Например, для товара, находящегося по пути Детям/Электроника/... в это поле запишется 'Детям'."
    )
    category_lvl_2: Mapped[str] = mapped_column(
        comment="Вторая часть категории товара. Например, для товара по пути Детям/Электроника/... "
        "в это поле запишется 'Электроника'."
    )
    category_lvl_3: Mapped[str] = mapped_column(
        comment="Третья часть категории товара. Например, для товара по пути Детям/Электроника/... "
        "в это поле запишется 'Детская электроника'."
    )
    category_remaining: Mapped[str] = mapped_column(
        comment="Остаток категории товара, например, 'Игровая консоль/Игровые консоли'."
    )

    # Прочие поля
    features: Mapped[dict] = mapped_column(JSON, comment="Характеристики товара")
    rating_count: Mapped[int] = mapped_column(comment="Количество отзывов о товаре")
    rating_value: Mapped[float] = mapped_column(Double, comment="Рейтинг товара (0-5)")
    price_before_discounts: Mapped[float] = mapped_column(REAL, comment="Цена товара до скидок")
    discount: Mapped[float] = mapped_column(Double, comment="Скидка на товар")
    price_after_discounts: Mapped[float] = mapped_column(REAL, comment="Цена товара после скидок")
    bonuses: Mapped[int] = mapped_column(comment="Количество бонусов")
    sales: Mapped[int] = mapped_column(comment="Количество продаж")
    currency: Mapped[str] = mapped_column(comment="Валюта товара")
    barcode: Mapped[str] = mapped_column(comment="Штрихкод товара")

    # Поля для временных меток
    inserted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), comment="Дата и время вставки записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="Дата и время последнего обновления"
    )

    # Поле для списка UUID похожих товаров
    similar_sku: Mapped[list[PG_UUID]] = Column(ARRAY(PG_UUID(as_uuid=True)), comment="Список UUID похожих товаров")

    # Определение индексов и уникальных ограничений
    __table_args__ = (
        Index("sku_brand_index", "brand"),  # Индекс для ускорения поиска по бренду
        UniqueConstraint("marketplace_id", "product_id", name="sku_marketplace_id_sku_id_uindex"),
        # Уникальный индекс для marketplace_id и product_id
        UniqueConstraint("uuid", name="sku_uuid_uindex"),  # Уникальный индекс для uuid
    )

    def __repr__(self):
        """
        Возвращает строковое представление объекта SKU, которое удобно для отладки.
        """
        return (
            f"<SKU(uuid={self.uuid}, title={self.title}, price={self.price_after_discounts}, "
            f"similar_sku={self.similar_sku})>"
        )
