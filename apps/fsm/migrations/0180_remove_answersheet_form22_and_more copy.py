# Generated by Django 4.1.3 on 2024-09-25 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0179_certificatetemplate_registration_form2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answersheet',
            old_name='form',
            new_name='formc',
        ),
        migrations.RenameField(
            model_name='certificatetemplate',
            old_name='registration_form',
            new_name='registration_formc',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='registration_form',
            new_name='registration_formc',
        ),
        migrations.RenameField(
            model_name='answersheet',
            old_name='form22',
            new_name='form',
        ),
        migrations.RenameField(
            model_name='certificatetemplate',
            old_name='registration_form2',
            new_name='registration_form',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='registration_form2',
            new_name='registration_form',
        ),
    ]
