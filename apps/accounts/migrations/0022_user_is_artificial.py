# Generated by Django 4.1.3 on 2024-06-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_userwebsite_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_artificial',
            field=models.BooleanField(default=False),
        ),
    ]
