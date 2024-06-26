# Generated by Django 4.1.3 on 2024-06-09 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_rename_is_event_owner_member_is_program_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWebsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_websites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
