# Generated by Django 4.1.3 on 2024-05-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_verificationcode_verification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='callback_domain',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
