from django.contrib import admin
from .models import Farmer,Profile, BillingAddress

class FarmerAdmin(admin.ModelAdmin):
    list_display = ['name','image','contact']

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['username','email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','phone']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city']

# Register your models here.
admin.site.register(Farmer,FarmerAdmin)
# admin.site.register(Customer,CustomerAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(BillingAddress,AddressAdmin)