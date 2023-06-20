# Generated by Django 4.1.7 on 2023-06-20 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_form', '0001_initial'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='my_form.registrationreceipt'),
        ),
        migrations.AddField(
            model_name='group',
            name='head',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_group', to='my_form.registrationreceipt'),
        ),
        migrations.AddField(
            model_name='group',
            name='registration_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='my_form.registrationform'),
        ),
    ]