# Generated by Django 4.1.3 on 2024-09-11 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0165_rename__attributes_object_attributes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='show_appbar',
            field=models.BooleanField(default=True),
        ),
    ]
