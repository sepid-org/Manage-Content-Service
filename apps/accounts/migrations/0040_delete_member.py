# Generated by Django 4.1.3 on 2024-08-30 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_discountcode_discount_code_limit'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Member',
        ),
    ]
