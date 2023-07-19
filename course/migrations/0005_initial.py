# Generated by Django 4.1.7 on 2023-06-20 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_form', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0014_alter_educationalinstitute_polymorphic_ctype_and_more'),
        ('course', '0004_delete_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='courses/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('type', models.CharField(choices=[('Group', 'Group'), ('Individual', 'Individual')], default='Individual', max_length=40)),
                ('team_size', models.IntegerField(default=3)),
                ('maximum_participant', models.IntegerField(blank=True, null=True)),
                ('accessible_after_closure', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('merchandise', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course', to='accounts.merchandise')),
                ('organizer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='accounts.educationalinstitute')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
                ('registration_form', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course', to='my_form.registrationform')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]