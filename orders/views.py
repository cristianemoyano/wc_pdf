import logging

from django.shortcuts import render
from django.core.cache import cache

from woocommerce import API

import os

logger = logging.getLogger(__name__)

CACHING_TIMEOUT = 10 * 60

def get_wc_api_client():
    try:
        return API(
            url=os.environ.get('WC_API_URL'),
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

def order_list(request):
    client = get_wc_api_client()
    orders = get_orders(client)
    return render(request, 'orders/list.html', {'orders': orders})
