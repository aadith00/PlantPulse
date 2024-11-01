from django.contrib import admin
from .models import Farmer, BillingAddress, Customer

class FarmerAdmin(admin.ModelAdmin):
    list_display = ['name','image','contact']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','phone']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name']

# Register your models here.
admin.site.register(Farmer,FarmerAdmin)
admin.site.register(BillingAddress,AddressAdmin)
admin.site.register(Customer,CustomerAdmin)