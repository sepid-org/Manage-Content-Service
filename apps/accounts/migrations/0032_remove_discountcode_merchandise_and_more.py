# Generated by Django 4.1.3 on 2024-08-09 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_discountcode_merchandise2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discountcode',
            name='merchandise',
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='merchandise2',
            field=models.ManyToManyField(related_name='discount_codes', to='accounts.merchandise'),
        ),
    ]
