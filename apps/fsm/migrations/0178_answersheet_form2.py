# Generated by Django 4.1.3 on 2024-09-25 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0177_alter_program_registration_form2'),
    ]

    operations = [
        migrations.AddField(
            model_name='answersheet',
            name='form22',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='answer_sheets', to='fsm.registrationform2'),
        ),
    ]
