import uuid
from datetime import datetime

from sqlalchemy import ARRAY, JSON, REAL, TIMESTAMP, BigInteger, Column, Double, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    # __tablename__ = 'base'
    pass


class SKU(Base):
    __tablename__ = "sku"

    uuid: Mapped[PG_UUID] = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id товара в нашей бд",
    )
    marketplace_id: Mapped[int] = mapped_column(nullable=False, comment="id маркетплейса")
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="id товара в маркетплейсе")
    title: Mapped[str] = mapped_column(comment="название товара")
    description: Mapped[str] = mapped_column(comment="описание товара")
    brand: Mapped[str] = mapped_column(index=True)
    seller_id: Mapped[int]
    seller_name: Mapped[str]
    first_image_url: Mapped[str]
    category_id: Mapped[int]
    category_lvl_1: Mapped[str] = mapped_column(
        comment="Первая часть категории товара. "
        "Например, для товара, находящегося по пути Детям/Электроника/"
        "Детская электроника/Игровая консоль/Игровые консоли и игры/"
        'Игровые консоли, в это поле запишется "Детям".'
    )
    category_lvl_2: Mapped[str] = mapped_column(
        comment="Вторая часть категории товара. "
        "Например, для товара, находящегося по пути Детям/Электроника/"
        "Детская электроника/Игровая консоль/Игровые консоли и игры/"
        'Игровые консоли, в это поле запишется "Электроника".'
    )
    category_lvl_3: Mapped[str] = mapped_column(
        comment="Третья часть категории товара. "
        "Например, для товара, находящегося по пути Детям/Электроника/"
        "Детская электроника/Игровая консоль/Игровые консоли и игры/"
        'Игровые консоли, в это поле запишется "Детская электроника".'
    )
    category_remaining: Mapped[str] = mapped_column(
        comment="Остаток категории товара. Например, для товара, "
        "находящегося по пути Детям/Электроника/Детская электроника/"
        "Игровая консоль/Игровые консоли и игры/Игровые консоли, "
        'в это поле запишется "Игровая консоль/Игровые консоли и игры/Игровые консоли".'
    )
    features: Mapped[dict] = mapped_column(JSON, comment="Характеристики товара")
    rating_count: Mapped[int] = mapped_column(comment="Кол-во отзывов о товаре")
    rating_value: Mapped[float] = mapped_column(Double, comment="Рейтинг товара (0-5)")
    price_before_discounts: Mapped[float] = mapped_column(REAL)
    discount: Mapped[float] = mapped_column(Double)
    price_after_discounts: Mapped[float] = mapped_column(REAL)
    bonuses: Mapped[int]
    sales: Mapped[int]
    inserted_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    currency: Mapped[str]
    barcode: Mapped[str] = mapped_column(comment="Штрихкод")
    similar_sku: Mapped[list[PG_UUID]] = Column(ARRAY(PG_UUID(as_uuid=True)))

    __table_args__ = (
        Index("sku_brand_index", "brand"),  # Индекс для колонки 'brand'
        UniqueConstraint("marketplace_id", "product_id", name="sku_marketplace_id_sku_id_uindex"),  # Уникальный индекс
        UniqueConstraint("uuid", name="sku_uuid_uindex"),
        # Уникальный индекс для uuid
    )

    def __repr__(self):
        return (
            f"<SKU(uuid={self.uuid}, title={self.title}, price={self.price_after_discounts}, "
            f"similar_sku={self.similar_sku})>"
        )
