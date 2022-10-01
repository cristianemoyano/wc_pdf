from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('orders/list/json', views.order_list_json, name='order_list_api'),
    path(
        'orders/<int:order_id>/pdf',
        views.order_pdf,
        name="order_pdf",
    ),
]