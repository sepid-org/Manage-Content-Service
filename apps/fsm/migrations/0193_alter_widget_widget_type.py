# Generated by Django 4.1.3 on 2024-10-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0192_rename_boxwidget_placeholder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='widget_type',
            field=models.CharField(choices=[('Iframe', 'Iframe'), ('Video', 'Video'), ('Image', 'Image'), ('Aparat', 'Aparat'), ('Audio', 'Audio'), ('TextWidget', 'Textwidget'), ('Placeholder', 'Placeholder'), ('DetailBoxWidget', 'Detailboxwidget'), ('SmallAnswerProblem', 'Smallanswerproblem'), ('BigAnswerProblem', 'Biganswerproblem'), ('MultiChoiceProblem', 'Multichoiceproblem'), ('UploadFileProblem', 'Uploadfileproblem'), ('ButtonWidget', 'Buttonwidget'), ('CustomWidget', 'Customwidget')], max_length=30),
        ),
    ]
