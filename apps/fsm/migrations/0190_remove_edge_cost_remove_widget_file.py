# Generated by Django 4.1.3 on 2024-09-30 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0189_remove_edge_cost_remove_widget_is_hidden_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widget',
            name='file',
        ),
        migrations.RemoveField(
            model_name='edge',
            name='cost',
        ),
    ]