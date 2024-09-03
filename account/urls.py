from django.urls import path
from .views import account, wishlist,auth

urlpatterns = [
    path('account', account, name='my-account'),
    path('wishlist', wishlist, name='wishlist'),
    path('auth', auth, name = 'auth'),
]