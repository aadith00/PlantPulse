from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','status','created_at']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'created_at', 'status']

admin.register(Cart,CartAdmin)
admin.register(CartItem)
admin.register(Order,OrderAdmin)