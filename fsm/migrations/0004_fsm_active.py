# Generated by Django 3.0.8 on 2020-09-07 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0003_auto_20200901_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='fsm',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]