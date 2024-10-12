from django.contrib import admin
from .models import Farmer,Profile

class FarmerAdmin(admin.ModelAdmin):
    list_display = ['name','image','contact']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username','email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','phone']

# Register your models here.
admin.site.register(Farmer,FarmerAdmin)
# admin.site.register(Customer,CustomerAdmin)
admin.site.register(Profile,ProfileAdmin)
