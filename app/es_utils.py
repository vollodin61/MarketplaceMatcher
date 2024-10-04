import uuid

from elasticsearch import AsyncElasticsearch


async def init_es(es_url: str) -> AsyncElasticsearch:
    """
    Инициализация клиента Elasticsearch.

    Args:
        es_url (str): URL сервера Elasticsearch.

    Returns:
        AsyncElasticsearch: Асинхронный клиент для работы с Elasticsearch.
    """
    # Создаем клиент Elasticsearch
    es_client = AsyncElasticsearch(hosts=[es_url])
    return es_client


async def index_in_elasticsearch(es_client: AsyncElasticsearch, sku) -> None:
    """
    Индексирует SKU (товар) в Elasticsearch.

    Args:
        es_client (AsyncElasticsearch): Клиент Elasticsearch для взаимодействия с сервером.
        sku: Объект SKU, содержащий данные для индексации, включая такие поля, как marketplace_id,
        title, description и т.д.

    Returns:
        None
    """
    # Подготавливаем данные для индексации
    data = {
        "marketplace_id": sku.marketplace_id,
        "product_id": sku.product_id,
        "title": sku.title,
        "description": sku.description,
        "brand": sku.brand,
        "seller_id": sku.seller_id,
        "seller_name": sku.seller_name,
        "first_image_url": sku.first_image_url,
        "category_id": sku.category_id,
        "category_lvl_1": sku.category_lvl_1,
        "category_lvl_2": sku.category_lvl_2,
        "category_lvl_3": sku.category_lvl_3,
        "category_remaining": sku.category_remaining,
        "features": sku.features,
        "rating_count": sku.rating_count,
        "rating_value": sku.rating_value,
        "price_before_discounts": sku.price_before_discounts,
        "discount": sku.discount,
        "price_after_discounts": sku.price_after_discounts,
        "bonuses": sku.bonuses,
        "sales": sku.sales,
        "currency": sku.currency,
        "barcode": sku.barcode,
    }

    try:
        # Индексация документа в Elasticsearch
        await es_client.index(index="sku", id=str(sku.uuid), document=data)
        print(f"{'_' * 29} Successfully indexed SKU {sku.uuid}")
    except Exception as e:
        # Обработка ошибок при индексации
        print(f"Failed to index SKU {sku.uuid}: {e}")


async def find_similar_skus(es_client: AsyncElasticsearch, sku) -> list[uuid.UUID]:
    """
    Находит похожие SKU с помощью запроса "more_like_this" в Elasticsearch.

    Args:
        es_client (AsyncElasticsearch): Клиент Elasticsearch для взаимодействия с сервером.
        sku: Объект SKU, для которого необходимо найти похожие элементы.

    Returns:
        list[uuid.UUID]: Список UUID похожих SKU.
    """
    # Формируем запрос "more_like_this" для поиска похожих товаров
    query = {
        "size": 5,
        "query": {
            "more_like_this": {
                "fields": ["title", "description", "brand", "features"],
                "like": [{"_id": str(sku.uuid)}],
                "min_term_freq": 1,
                "max_query_terms": 12,
            }
        },
    }

    try:
        # Выполнение поиска по индексу
        response = await es_client.search(index="sku", body=query)
        hits = response.get("hits", {}).get("hits", [])
        similar = [uuid.UUID(hit["_id"]) for hit in hits]
        print(f"{'_' * 29} Found {len(similar)} similar SKUs for {sku.uuid}")
        return similar
    except Exception as e:
        # Обработка ошибок при поиске похожих товаров
        print(f"Failed to search similar SKUs for {sku.uuid}: {e.__repr__()}")
        return []
