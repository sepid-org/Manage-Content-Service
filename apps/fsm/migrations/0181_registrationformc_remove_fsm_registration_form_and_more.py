# Generated by Django 4.1.3 on 2024-09-25 16:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0180_remove_answersheet_form22_and_more copy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RegistrationForm',
            new_name='RegistrationFormC',
        ),
        migrations.RenameModel(
            old_name='RegistrationForm2',
            new_name='RegistrationForm',
        ),
    ]
