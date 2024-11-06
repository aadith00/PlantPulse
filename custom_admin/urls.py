from django.urls import path
from .views import (
    dashboard,
    add_product,
    update_product,
    delete_product,
    manage_orders,
    update_order_status,
    admin_logout,
    manage_users,
    edit_user,
    add_user,
    order_confirmation,
    delete_user,
    view_order,
    delete_order
)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('add_user/', add_user, name='add_user'),
    path('custom_admin/add_product/', add_product, name='add_product'),
    path('custom_admin/update_product/<str:product_id>/', update_product, name='update_product'),
    path('custom_admin/delete_product/<str:product_id>/', delete_product, name='delete_product'),
    path('orders/', manage_orders, name='manage_orders'),
    path('orders/view_order/<int:order_id>', view_order, name='view_order'),
    path('order/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('custom_admin/update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('logout/', admin_logout, name='logout')
]
