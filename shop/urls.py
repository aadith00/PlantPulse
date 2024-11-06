from django.urls import path
from .views import checkout, shop_detail, product_detail, add_to_cart, cart, remove_from_cart, checkoutpage, payment, order_confirmation
from . import views

# urls
urlpatterns = [
    path('cart/', cart, name='cart'),
    path('checkoupage', checkoutpage , name='checkoutpage'),
    path('shopdetail', shop_detail, name='shop-detail'),
    path('product/<pid>/', product_detail, name='product-detail'),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/<int:id>', payment, name='payment'),
    path('order_confirmation_user/<uuid:order_id>/', order_confirmation, name ='order_confirmation_user'),
]
