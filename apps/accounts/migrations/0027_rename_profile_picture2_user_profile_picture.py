# Generated by Django 4.1.3 on 2024-08-02 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_remove_user_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_picture2',
            new_name='profile_picture',
        ),
    ]
