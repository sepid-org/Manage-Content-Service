# Generated by Django 4.1.3 on 2024-08-08 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0147_remove_registrationform_conditions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fsm',
            name='merchandise',
        ),
        migrations.RemoveField(
            model_name='program',
            name='merchandise',
        ),
    ]
