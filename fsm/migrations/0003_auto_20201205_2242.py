# Generated by Django 3.0.8 on 2020-12-05 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0002_auto_20201205_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('cover_page', models.ImageField(blank=True, null=True, upload_to='workshop/')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='fsm',
            name='fsm_p_type',
            field=models.CharField(choices=[('team', 'Team'), ('individual', 'Individual'), ('hybrid', 'Hybrid')], default='individual', max_length=40),
        ),
        migrations.AddField(
            model_name='fsm',
            name='event',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fsm.Event'),
        ),
    ]