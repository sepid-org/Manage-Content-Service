# Generated by Django 4.1.3 on 2024-09-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0169_state_is_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]