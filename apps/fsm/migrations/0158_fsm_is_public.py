# Generated by Django 4.1.3 on 2024-08-30 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0157_remove_program_holder'),
    ]

    operations = [
        migrations.AddField(
            model_name='fsm',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
