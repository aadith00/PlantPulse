from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe

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