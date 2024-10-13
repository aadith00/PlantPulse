from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Farmer(models.Model):
    far_id = ShortUUIDField(unique=True, length = 10, max_length=30, prefix="far")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    decription = models.TextField(null=True, blank=True)

    address = models.CharField(max_length=100, default="India")
    contact = models.CharField(max_length=100, default="+91XXX XXX XXXX")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Farmers"

    def farmer_image(self):
        return mark_safe('<img src= "%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.name
    

# class Customer(AbstractUser):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=100)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.address}, {self.city}'
    
