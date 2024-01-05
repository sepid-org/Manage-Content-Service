# Generated by Django 4.1.3 on 2024-01-05 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_user_phone_number'),
        ('scoring', '0012_cost_reward_transaction_remove_comment_writer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoretype',
            name='institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='score_types', to='accounts.educationalinstitute'),
        ),
    ]