from django.db import models
from django.contrib.auth.models import User
from tomatoes.models import Product
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='in_progress')  # in_progress, completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Product price at the time of adding to cart

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in {self.cart.user.username}'s cart"
    
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, default=" ")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    delivery_time=models.TextField(max_length=255,null=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username} - Total: {self.total_price}"
    
class ContactUs(models.Model):
    name=models.TextField(max_length=255)
    email=models.TextField(max_length=255)
    subject=models.TextField(max_length=255)
    message=models.TextField(max_length=555)
    status=models.BooleanField(default=True)