# Generated by Django 4.1.3 on 2024-08-01 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0146_alter_registrationreceipt_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationform',
            name='conditions',
        ),
    ]
