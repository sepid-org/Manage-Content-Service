# Generated by Django 4.1.3 on 2024-08-19 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0152_problem_correctness_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
