from django.urls import path
from .views import dashboard,manage_orders,admin_logout,manage_users,edit_user,add_user,order_confirmation,delete_user,view_order,delete_order,manage_products, view_messages

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('add_user/', add_user, name='add_user'),
    path('orders/', manage_orders, name='manage_orders'),
    path('orders/view_order/<int:order_id>', view_order, name='view_order'),
    path('order/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('manage_products/', manage_products, name='manage_products'),
    path('view-messages/', view_messages, name='view_messages'),
    path('logout/', admin_logout, name='logout')
]
