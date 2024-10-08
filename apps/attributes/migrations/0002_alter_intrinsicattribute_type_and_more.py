# Generated by Django 4.1.3 on 2024-08-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intrinsicattribute',
            name='type',
            field=models.CharField(choices=[('cost', 'Cost'), ('reward', 'Reward'), ('required_balance', 'Required Balance'), ('password', 'Password')], max_length=20),
        ),
        migrations.AlterField(
            model_name='performableaction',
            name='type',
            field=models.CharField(choices=[('see', 'See'), ('purchase', 'Purchase'), ('sell', 'Sell'), ('copy', 'Copy'), ('solve', 'Solve'), ('attempt', 'Attempt'), ('enter', 'Enter')], max_length=20),
        ),
    ]
