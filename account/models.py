from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import User
import random

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Farmer(models.Model):
    far_id = ShortUUIDField(unique=True, length = 10, max_length=30, prefix="far")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    decription = models.TextField(null=True, blank=True)

    address = models.CharField(max_length=100, default="India")
    contact = models.CharField(max_length=100, default="+91XXX XXX XXXX")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Farmers"

    def farmer_image(self):
        return mark_safe('<img src= "%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=8, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Address Information
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default=" ", blank=True, null=True)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    # Preferences and Status
    preferred_contact_method = models.CharField(max_length=10, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS')
    ], default='email')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.customer_id:
            unique_number = ''.join([str(random.randint(0, 9)) for _ in range(5)])
            self.customer_id = f"CUS{unique_number}"
        super().save(*args, **kwargs)