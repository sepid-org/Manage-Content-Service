# Generated by Django 4.1.3 on 2024-09-25 11:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0175_rename_form2_answersheet_form_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('paper_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fsm.paper')),
                ('audience_type', models.CharField(choices=[('Student', 'Student'), ('Academic', 'Academic'), ('All', 'All')], default='All', max_length=50)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fsm.paper',),
        ),
        migrations.CreateModel(
            name='RegistrationForm2',
            fields=[
                ('form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fsm.form')),
                ('min_grade', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)])),
                ('max_grade', models.IntegerField(default=12, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)])),
                ('accepting_status', models.CharField(choices=[('AutoAccept', 'Autoaccept'), ('CorrectAccept', 'Correctaccept'), ('Manual', 'Manual')], default='AutoAccept', max_length=15)),
                ('gender_partition_status', models.CharField(choices=[('OnlyMale', 'Onlymale'), ('OnlyFemale', 'Onlyfemale'), ('BothPartitioned', 'Bothpartitioned'), ('BothNonPartitioned', 'Bothnonpartitioned')], default='BothPartitioned', max_length=25)),
                ('has_certificate', models.BooleanField(default=False)),
                ('certificates_ready', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fsm.form',),
        ),
        migrations.AddField(
            model_name='program',
            name='registration_form2',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='program', to='fsm.registrationform2'),
        ),
    ]
