# Generated by Django 4.1.3 on 2023-11-13 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0076_article_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='fsm',
            name='order_in_program',
            field=models.IntegerField(default=0),
        ),
    ]
