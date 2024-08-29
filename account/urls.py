from django.urls import path
from .views import account, wishlist

urlpatterns = [
    path('account', account, name='my-account'),
    path('wishlist', wishlist, name='wishlist'),
]