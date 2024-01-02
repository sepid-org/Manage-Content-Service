# Generated by Django 4.1.3 on 2024-01-01 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_remove_group_head_remove_group_registration_form_and_more'),
        # ('course', '0007_delete_course'),
        ('fsm', '0087_remove_newstate_fsm_remove_newstate_paper_ptr_and_more'),
        ('my_form', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='receipt',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='deliverable_ptr',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='form',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='user',
        ),
        migrations.RemoveField(
            model_name='registrationform',
            name='form_ptr',
        ),
        migrations.RemoveField(
            model_name='registrationreceipt',
            name='group',
        ),
        migrations.RemoveField(
            model_name='registrationreceipt',
            name='receipt_ptr',
        ),
        migrations.DeleteModel(
            name='Form',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
        migrations.DeleteModel(
            name='RegistrationForm',
        ),
        migrations.DeleteModel(
            name='RegistrationReceipt',
        ),
    ]
