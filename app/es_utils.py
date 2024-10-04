import uuid

from elasticsearch import AsyncElasticsearch


async def init_es(es_url: str, username: str, password: str):
    # Создаем клиент Elasticsearch
    es_client = AsyncElasticsearch(hosts=[es_url], http_auth=(username, password))
    return es_client


async def index_in_elasticsearch(es_client: AsyncElasticsearch, sku):
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
        await es_client.index(index="sku", id=str(sku.uuid), document=data)
    except Exception as e:
        print(f"Failed to index SKU {sku.uuid}: {e}")


async def find_similar_skus(es_client: AsyncElasticsearch, sku) -> list[uuid.UUID]:
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
        response = await es_client.search(index="sku", body=query)
        hits = response.get("hits", {}).get("hits", [])
        similar = [uuid.UUID(hit["_id"]) for hit in hits]
        return similar
    except Exception as e:
        print(f"Failed to search similar SKUs for {sku.uuid}: {e}")
        return []
