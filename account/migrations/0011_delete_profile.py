# Generated by Django 5.1 on 2024-11-01 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_farmer_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
