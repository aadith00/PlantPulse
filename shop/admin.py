from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'created_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price')
    search_fields = ('product__title', 'cart__user__username')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username', 'status', 'order_id')
    list_filter = ('status', 'created_at')

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status')
    search_fields = ('name', 'email')
    list_filter = ('status',)

# Register models with custom admin classes
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ContactUs, ContactUsAdmin)