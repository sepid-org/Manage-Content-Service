# Generated by Django 4.1.3 on 2024-09-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0170_program_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='template',
        ),
        migrations.AddField(
            model_name='paper',
            name='template',
            field=models.CharField(choices=[('normal', 'Normal'), ('board', 'Board')], default='normal', max_length=20),
        ),
    ]