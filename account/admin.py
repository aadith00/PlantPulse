from django.contrib import admin
from .models import Farmer,User,Profile

class FarmerAdmin(admin.ModelAdmin):
    list_display = ['name','image','contact']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','phone']

# Register your models here.
admin.site.register(Farmer,FarmerAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
