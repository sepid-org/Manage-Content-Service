# Generated by Django 4.1.3 on 2024-08-11 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_alter_merchandise_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentship',
            name='document2',
            field=models.URLField(max_length=2000, null=True),
        ),
    ]
