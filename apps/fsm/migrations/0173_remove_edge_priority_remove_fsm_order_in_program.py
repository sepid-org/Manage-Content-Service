# Generated by Django 4.1.3 on 2024-09-22 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0172_object_is_private_object_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edge',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='fsm',
            name='order_in_program',
        ),
    ]
