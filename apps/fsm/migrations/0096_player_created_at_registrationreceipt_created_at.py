# Generated by Django 4.1.3 on 2024-03-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0095_alter_event_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='registrationreceipt',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]