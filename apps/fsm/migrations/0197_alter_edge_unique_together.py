# Generated by Django 4.1.3 on 2024-10-08 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0196_rename_current_state2_player_current_state22'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='edge',
            unique_together={('tail', 'head')},
        ),
    ]
