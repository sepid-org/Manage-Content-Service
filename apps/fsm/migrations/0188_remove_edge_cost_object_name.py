# Generated by Django 4.1.3 on 2024-09-28 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0187_remove_edge_cost_alter_answersheet_form_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
