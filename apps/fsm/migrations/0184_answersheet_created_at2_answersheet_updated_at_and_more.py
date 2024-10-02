# Generated by Django 4.1.3 on 2024-09-26 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fsm', '0183_remove_answersheet_formc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answersheet',
            name='created_at2',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='answersheet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='answersheet',
            name='user2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_sheets', to=settings.AUTH_USER_MODEL),
        ),
    ]