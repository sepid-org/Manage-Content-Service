# Generated by Django 3.1 on 2021-10-28 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0036_auto_20211028_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatetemplate',
            name='font',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='templates', to='fsm.font'),
        ),
    ]