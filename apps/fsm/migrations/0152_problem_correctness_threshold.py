# Generated by Django 4.1.3 on 2024-08-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0151_widget_attributes_alter_widget_widget_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='correctness_threshold',
            field=models.IntegerField(default=100),
        ),
    ]
