# Generated by Django 4.1.3 on 2024-09-03 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0160_remove_team_registration_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='fsm.program'),
        ),
    ]
