# Generated by Django 4.1.3 on 2024-04-18 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0097_rename_game_iframe_alter_widget_widget_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='fsm',
            name='cover_page2',
            field=models.URLField(blank=True, null=True),
        ),
    ]
