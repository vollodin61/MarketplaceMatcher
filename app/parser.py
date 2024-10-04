import uuid
from typing import AsyncGenerator

import lxml.etree as ET

from app.models import SKU


def build_category_hierarchy(file_path: str):
    categories = {}
    parent_map = {}

    # Парсим файл до раздела <categories> для извлечения категорий
    context = ET.iterparse(file_path, events=("end",), tag="category")
    for event, elem in context:
        category_id = int(elem.get("id"))
        parent_id = elem.get("parentId")
        parent_id = int(parent_id) if parent_id else None
        categories[category_id] = elem.text
        parent_map[category_id] = parent_id
        elem.clear()  # Очищаем элемент для освобождения памяти

    return categories, parent_map


def get_category_path(category_id, categories, parent_map):
    # Получаем путь к категории
    path = []
    current_id = category_id
    while current_id:
        category_name = categories.get(current_id)
        if category_name:
            path.insert(0, category_name)
        current_id = parent_map.get(current_id)
    return path


def parse_features(elem: ET.Element) -> dict:
    features = {}
    for feature in elem.findall(".//features/feature"):
        key = feature.findtext("name")
        value = feature.findtext("value")
        if key and value:
            features[key] = value
    return features


async def parse_xml(file_path: str, categories, parent_map) -> AsyncGenerator[SKU, None]:
    context = ET.iterparse(file_path, events=("end",), tag="offer")

    for _, elem in context:
        try:
            # Извлекаем информацию о товаре
            marketplace_id = elem.get("marketplace_id")
            product_id = elem.get("id")
            seller_id = elem.findtext("sellerId")
            category_id = elem.findtext("categoryId")

            # Получаем категорию товара и строим путь категорий
            category_id = int(category_id) if category_id else 0
            category_path = get_category_path(category_id, categories, parent_map)

            # Разбираем категории по уровням
            category_lvl_1 = category_path[0] if len(category_path) > 0 else ""
            category_lvl_2 = category_path[1] if len(category_path) > 1 else ""
            category_lvl_3 = category_path[2] if len(category_path) > 2 else ""
            category_remaining = "/".join(category_path[3:]) if len(category_path) > 3 else ""

            # Создаем объект SKU с заполненными полями
            sku = SKU(
                uuid=uuid.uuid4(),
                marketplace_id=int(marketplace_id) if marketplace_id is not None else 0,
                product_id=int(product_id) if product_id is not None else 0,
                title=elem.findtext("name") or "",
                description=elem.findtext("description") or "",
                brand=elem.findtext("vendor") or "",
                seller_id=int(seller_id) if seller_id is not None else 0,
                seller_name=elem.findtext("sellerName") or "",
                first_image_url=elem.findtext("picture") or "",
                category_id=category_id,
                category_lvl_1=category_lvl_1,
                category_lvl_2=category_lvl_2,
                category_lvl_3=category_lvl_3,
                category_remaining=category_remaining,
                features=parse_features(elem),
                rating_count=(int(elem.findtext("rating_count")) if elem.findtext("rating_count") else 0),
                rating_value=(float(elem.findtext("rating_value")) if elem.findtext("rating_value") else 0.0),
                price_before_discounts=(
                    float(elem.findtext("price_before_discounts")) if elem.findtext("price_before_discounts") else 0.0
                ),
                discount=(float(elem.findtext("discount")) if elem.findtext("discount") else 0.0),
                price_after_discounts=(
                    float(elem.findtext("price_after_discounts")) if elem.findtext("price_after_discounts") else 0.0
                ),
                bonuses=(int(elem.findtext("bonuses")) if elem.findtext("bonuses") else 0),
                sales=int(elem.findtext("sales")) if elem.findtext("sales") else 0,
                currency=elem.findtext("currency") or "",
                barcode=(str(elem.findtext("barcode")) if elem.findtext("barcode") else ""),
                similar_sku=[],  # Инициализируем пустым списком
            )
            yield sku
        except Exception as e:
            print(f"Error parsing element: {e}")
        finally:
            elem.clear()  # Очищаем элемент для экономии памяти
