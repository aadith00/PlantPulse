from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import User


STATUS_CHOICE = (
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),
)

STATUS = [
    ('in_review', 'In Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

RATING = (
    (1," ★ ☆ ☆ ☆ ☆"),
    (2," ★ ★ ☆ ☆ ☆"),
    (3," ★ ★ ★ ☆ ☆"),
    (4," ★ ★ ★ ★ ☆"),
    (5," ★ ★ ★ ★ ★")
)

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)

# Create your models here.
class Variety(models.Model):
    var_id = ShortUUIDField(unique=True, length = 10, max_length=30, prefix="var")
    name = models.CharField(max_length=100)
    price_per_kg = models.IntegerField(max_length=5)
    image = models.ImageField(upload_to="Variety")

    class Meta:
        verbose_name_plural = "Varieties"

    def variety_image(self):
        return mark_safe('<img src= "%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="prd")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Fresh Tomato")
    image = models.ImageField(upload_to="Products", default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    life = models.CharField(max_length=100, default="14", null=True, blank=True)
    mfg_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", default="sku0000")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

class ProductImages(models.Model):
    images = models.ImageField(upload_to = "product-images",default="product.jpg")  
    product = models.ForeignKey(Product, related_name='p_image', on_delete=models.SET_NULL,null= True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

class CartOrder(models.Model):
    user = models.ForeignKey(Product, on_delete=models.SET_NULL,null= True)
    price = models.DecimalField(max_digits=99999999999999,decimal_places=2,default="0")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices = STATUS_CHOICE, max_length=30,default="in_review")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200, default="XX")
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Cart Order Items")
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999999,decimal_places=2,default="1.99")
    total = models.DecimalField(max_digits=99999999999999,decimal_places=2,default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src = "/media/%s" width = "50" height = "50" />' % (self.image))
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null= True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices = RATING,default = None)
    date = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def  get_rating(self):
        return self.rating

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100,null = True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

class Disease(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    causes = models.TextField()
    image = models.ImageField(upload_to="Diseases")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Diseases"