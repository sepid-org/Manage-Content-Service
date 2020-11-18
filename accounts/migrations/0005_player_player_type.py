# Generated by Django 3.0.8 on 2020-11-10 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201109_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='player_type',
            field=models.CharField(choices=[('TEAM', 'Team'), ('PARTICIPANT', 'Participant')], default='TEAM', max_length=15),
        ),
    ]