# Generated by Django 5.1 on 2024-11-05 18:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_customer_state_delete_billingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='last_order_date',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='order_count',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='total_spent',
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=12, unique=True),
        ),
    ]
