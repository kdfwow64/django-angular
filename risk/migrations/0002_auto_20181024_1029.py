# Generated by Django 2.0.5 on 2018-10-24 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='desc_alt',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='desc_form',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='example_content1',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='example_content2',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='example_image1',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='example_image2',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='example_title1',
        ),
        migrations.RemoveField(
            model_name='timeunit',
            name='example_title2',
        ),
        migrations.AddField(
            model_name='timeunit',
            name='abbrv',
            field=models.CharField(blank=True, help_text='Abbreviation of the name', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='company',
            field=models.ForeignKey(default=1, help_text='Company id for the company that manages the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_timeunit_related_company', to='risk.Company'),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='created_by',
            field=models.ForeignKey(default=13, help_text='User id of the user that created the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_timeunit_related_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-10-14 14:32:31.257000', help_text='Timestamp the field was created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeunit',
            name='date_deactivated',
            field=models.DateTimeField(blank=True, help_text='Timestamp the field was last deactivated', null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='date_deleted',
            field=models.DateTimeField(blank=True, help_text='Timestamp the individual was created', null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp the field was last modified', null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='deactivated_by',
            field=models.ForeignKey(blank=True, help_text='User id that last deactivated the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_timeunit_related_deactivated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='deleted_by',
            field=models.ForeignKey(blank=True, help_text='User id that last deleted the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_timeunit_related_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='example1',
            field=models.TextField(blank=True, help_text='Pratcial example of the category', null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='example2',
            field=models.TextField(blank=True, help_text='Pratcial example of the category', null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this field row should be treated as an active field and availiable for use by the application'),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='Designates whether this field row has been deleted'),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='keywords',
            field=models.TextField(blank=True, help_text='Keywords used to idenify proper category or find correct field name', null=True),
        ),
        migrations.AddField(
            model_name='timeunit',
            name='modified_by',
            field=models.ForeignKey(default=13, help_text='User id that last modified the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_timeunit_related_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timeunit',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the field', null=True),
        ),
        migrations.AlterField(
            model_name='timeunit',
            name='name',
            field=models.CharField(blank=True, help_text='Name of the field', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='timeunit',
            name='sort_order',
            field=models.IntegerField(blank=True, help_text='Sort order the field should be in for form selection', null=True),
        ),
    ]