# Generated by Django 3.2.7 on 2024-11-06 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
