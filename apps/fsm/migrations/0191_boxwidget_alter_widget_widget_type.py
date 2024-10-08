# Generated by Django 4.1.3 on 2024-10-02 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0190_remove_edge_cost_remove_widget_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fsm.widget')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('fsm.widget',),
        ),
        migrations.AlterField(
            model_name='widget',
            name='widget_type',
            field=models.CharField(choices=[('Iframe', 'Iframe'), ('Video', 'Video'), ('Image', 'Image'), ('Aparat', 'Aparat'), ('Audio', 'Audio'), ('TextWidget', 'Textwidget'), ('BoxWidget', 'Boxwidget'), ('DetailBoxWidget', 'Detailboxwidget'), ('SmallAnswerProblem', 'Smallanswerproblem'), ('BigAnswerProblem', 'Biganswerproblem'), ('MultiChoiceProblem', 'Multichoiceproblem'), ('UploadFileProblem', 'Uploadfileproblem')], max_length=30),
        ),
    ]
