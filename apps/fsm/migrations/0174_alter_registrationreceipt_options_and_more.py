# Generated by Django 4.1.3 on 2024-09-25 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0173_remove_edge_priority_remove_fsm_order_in_program'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationreceipt',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterUniqueTogether(
            name='registrationreceipt',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='answersheet',
            name='form2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='answer_sheets', to='fsm.registrationform'),
        ),
        migrations.AlterField(
            model_name='answersheet',
            name='answer_sheet_type',
            field=models.CharField(choices=[('RegistrationReceipt', 'Registrationreceipt'), ('StateAnswerSheet', 'Stateanswersheet'), ('General', 'General')], max_length=25),
        ),
    ]
