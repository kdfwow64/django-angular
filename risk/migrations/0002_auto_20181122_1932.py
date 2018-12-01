# Generated by Django 2.1.3 on 2018-11-23 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this field row should be treated as an active field and availiable for use by the application')),
                ('is_deleted', models.BooleanField(default=False, help_text='Designates whether this field row has been deleted')),
                ('date_created', models.DateTimeField(editable=False, help_text='Timestamp the field was created')),
                ('date_modified', models.DateTimeField(blank=True, help_text='Timestamp the field was last modified', null=True)),
                ('date_deactivated', models.DateTimeField(blank=True, help_text='Timestamp the field was last deactivated', null=True)),
                ('date_deleted', models.DateTimeField(blank=True, help_text='Timestamp the individual was created', null=True)),
                ('name', models.CharField(blank=True, help_text='Name of the field', max_length=128, null=True)),
                ('description', models.TextField(blank=True, help_text='Description of the field', null=True)),
                ('bkof_notes', models.TextField(blank=True, help_text='Backoffice notes.  DO NOT SHARE')),
                ('abbrv', models.CharField(blank=True, help_text='Abbreviation of the name', max_length=30, null=True)),
                ('sort_order', models.IntegerField(blank=True, default=0, help_text='Sort order the field should be in for form selection', null=True)),
                ('keywords', models.TextField(blank=True, help_text='Keywords used to idenify proper category or find correct field name', null=True)),
                ('under_review', models.BooleanField(default=False, help_text='Designates whether this category has been marked for review')),
                ('example1', models.TextField(blank=True, help_text='Pratcial example of the category', null=True)),
                ('example2', models.TextField(blank=True, help_text='Pratcial example of the category', null=True)),
                ('company', models.ForeignKey(default=1, help_text='Company id for the company that manages the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_controlfamily_related_company', to='risk.Company')),
                ('created_by', models.ForeignKey(default=13, help_text='User id of the user that created the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_controlfamily_related_created', to=settings.AUTH_USER_MODEL)),
                ('deactivated_by', models.ForeignKey(blank=True, help_text='User id that last deactivated the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_controlfamily_related_deactivated', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User id that last deleted the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_controlfamily_related_deleted', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(default=13, help_text='User id that last modified the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_controlfamily_related_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Control Families',
            },
        ),
        migrations.AddField(
            model_name='controlcategory',
            name='control_family',
            field=models.ForeignKey(help_text='Family that the control category belongs', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category_controlfamily', to='risk.ControlFamily'),
        ),
    ]