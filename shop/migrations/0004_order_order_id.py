# Generated by Django 5.1 on 2024-11-01 08:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
