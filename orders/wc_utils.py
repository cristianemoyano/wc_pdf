import os
import logging

from django.core.cache import cache
from woocommerce import API


logger = logging.getLogger(__name__)

CACHING_TIMEOUT = 10 * 60

def get_wc_api_client():
    try:
        logger.info("Connecting: %s", os.getenv("WC_API_URL"))
        return API(
            url=os.environ.get("WC_API_URL"),
            consumer_key=os.environ.get('WC_API_CONSUMER_KEY'),
            consumer_secret=os.environ.get('WC_API_CONSUMER_SECRET'),
            version="wc/v3",
        )
    except Exception as exc:
        logger.exception("Something went wrong: %s", exc)



def get_orders(client):
    if client is None:
        return []
    # https://woocommerce.github.io/woocommerce-rest-api-docs/?python#list-all-orders
    # cache.delete('wc_orders')
    if cache.get('wc_orders') is not None:
        return cache.get('wc_orders')
    orders = client.get("orders/?lang=es&per_page=10").json()
    cache.set('wc_orders', orders, CACHING_TIMEOUT)
    return orders

def get_order(client, order_id):
    if client is None:
        return []
    # https://woocommerce.github.io/woocommerce-rest-api-docs/?python#list-all-orders
    # cache.delete('wc_orders')
    if cache.get(f'wc_order_{order_id}') is not None:
        return cache.get(f'wc_order_{order_id}')
    order = client.get(f"orders/{order_id}").json()
    cache.set(f'wc_order_{order_id}', order, CACHING_TIMEOUT)
    return order
