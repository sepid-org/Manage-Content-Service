# Generated by Django 4.1.3 on 2024-08-09 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_remove_discountcode_merchandise_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountcode',
            old_name='merchandise2',
            new_name='merchandises',
        ),
    ]