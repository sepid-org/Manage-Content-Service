# Generated by Django 4.1.3 on 2024-06-04 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0134_fsm_deleted_at_program_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widget',
            name='duplication_of',
        ),
    ]