from django.contrib.auth.models import User
from django.db import models
import uuid

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    admin_id = models.CharField(max_length=10, unique=True, editable=False)  # Admin ID field
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.admin_id:
            self.admin_id = "ADM" + str(uuid.uuid4().int)[:7]  # Shortened UUID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"
