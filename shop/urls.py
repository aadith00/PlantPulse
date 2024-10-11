from django.urls import path
from .views import cart,checkout,shop_detail, product_detail, add_to_cart

#urls
urlpatterns = [
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('shopdetail', shop_detail, name='shop-detail'),
    path('product/<pid>/', product_detail, name='product-detail'),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
]