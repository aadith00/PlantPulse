from django.urls import path
from .views import account, wishlist,auth, user_register, user_login

urlpatterns = [
    path('account', account, name='my-account'),
    path('wishlist', wishlist, name='wishlist'),
    path('auth', auth, name = 'auth'),
    path('register', user_register, name='register'),
    path('login', user_login, name='login')
]