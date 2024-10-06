from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Variety)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(CartOrder)
admin.site.register(CartOrderItems)
admin.site.register(Address)