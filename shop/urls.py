from django.urls import path
from .views import cart,checkout,shop_detail,shop

#urls
urlpatterns = [
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('shopdetail', shop_detail, name='shop-detail'),
    path('shop', shop, name='shop'),
]

