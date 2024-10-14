from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Variety)

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

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'causes', 'image']


admin.site.register(Product,ProductAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Disease,DiseaseAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)

