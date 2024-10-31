from django.urls import path
from .views import (
    dashboard,
    add_product,
    update_product,
    delete_product,
    order_list,
    update_order_status,
)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('custom_admin/add_product/', add_product, name='add_product'),
    path('custom_admin/update_product/<str:product_id>/', update_product, name='update_product'),
    path('custom_admin/delete_product/<str:product_id>/', delete_product, name='delete_product'),
    path('custom_admin/orders/', order_list, name='order_list'),
    path('custom_admin/update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
]
