# Generated by Django 5.1 on 2024-11-05 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_order_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]
