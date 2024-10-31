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
    path('admin/dashboard/', dashboard, name='dashboard'),
    path('admin/add_product/', add_product, name='add_product'),
    path('admin/update_product/<str:product_id>/', update_product, name='update_product'),
    path('admin/delete_product/<str:product_id>/', delete_product, name='delete_product'),
    path('admin/orders/', order_list, name='order_list'),
    path('admin/update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
]
