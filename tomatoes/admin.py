from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Variety)
# admin.site.register(Product)
# admin.site.register(ProductImages)
# admin.site.register(CartOrder)
# admin.site.register(CartOrderItems)
# admin.site.register(ProductReview)
# admin.site.register(Address)

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','title','product_image','price','featured','product_status']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','order_date','product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','item','image','qty','price','total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','status']


admin.site.register(Product,ProductAdmin)
admin.site.register(Product,CartOrderAdmin)
admin.site.register(Product,CartOrderItemsAdmin)
admin.site.register(Product,AddressAdmin)