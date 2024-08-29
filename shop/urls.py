from django.urls import path
from .views import cart,checkout,shop_detail,shop

urlpatterns = [
    path('', cart, name='cart'),
    path('about', checkout, name='checkout'),
    path('contact', shop_detail, name='shop-detail'),
    path('gallery', shop, name='shop'),
     
]

