# Generated by Django 2.1.3 on 2019-04-05 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0012_auto_20190405_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectNextStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this field row should be treated as an active field and availiable for use by the application')),
                ('is_deleted', models.BooleanField(default=False, help_text='Designates whether this field row has been deleted')),
                ('is_test', models.BooleanField(default=False, help_text='Designates whether this field or content should be considered to be test data')),
                ('date_created', models.DateTimeField(editable=False, help_text='Timestamp the field was created')),
                ('date_activated', models.DateTimeField(editable=False, help_text='Timestamp the field was last activated')),
                ('date_modified', models.DateTimeField(blank=True, help_text='Timestamp the field was last modified', null=True)),
                ('date_deactivated', models.DateTimeField(blank=True, help_text='Timestamp the field was last deactivated', null=True)),
                ('date_deleted', models.DateTimeField(blank=True, help_text='Timestamp the individual was created', null=True)),
                ('summary', models.TextField(help_text='Summary of the next steps for the project')),
                ('is_enabled', models.BooleanField(default=True, help_text='Designates whether this topic should be present in the report')),
                ('activated_by', models.ForeignKey(default=13, help_text='User id that last activated the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectnextstep_related_activated', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(default=13, help_text='User id of the user that created the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectnextstep_related_created', to=settings.AUTH_USER_MODEL)),
                ('deactivated_by', models.ForeignKey(blank=True, help_text='User id that last deactivated the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectnextstep_related_deactivated', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User id that last deleted the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectnextstep_related_deleted', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(default=13, help_text='User id that last modified the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectnextstep_related_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Project Next Steps',
            },
        ),
        migrations.CreateModel(
            name='ProjectProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this field row should be treated as an active field and availiable for use by the application')),
                ('is_deleted', models.BooleanField(default=False, help_text='Designates whether this field row has been deleted')),
                ('is_test', models.BooleanField(default=False, help_text='Designates whether this field or content should be considered to be test data')),
                ('date_created', models.DateTimeField(editable=False, help_text='Timestamp the field was created')),
                ('date_activated', models.DateTimeField(editable=False, help_text='Timestamp the field was last activated')),
                ('date_modified', models.DateTimeField(blank=True, help_text='Timestamp the field was last modified', null=True)),
                ('date_deactivated', models.DateTimeField(blank=True, help_text='Timestamp the field was last deactivated', null=True)),
                ('date_deleted', models.DateTimeField(blank=True, help_text='Timestamp the individual was created', null=True)),
                ('summary', models.TextField(help_text='Summary of the topics for the project')),
                ('is_enabled', models.BooleanField(default=True, help_text='Designates whether this progress update should be present in the report')),
                ('activated_by', models.ForeignKey(default=13, help_text='User id that last activated the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectprogress_related_activated', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(default=13, help_text='User id of the user that created the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectprogress_related_created', to=settings.AUTH_USER_MODEL)),
                ('deactivated_by', models.ForeignKey(blank=True, help_text='User id that last deactivated the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectprogress_related_deactivated', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User id that last deleted the field', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectprogress_related_deleted', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(default=13, help_text='User id that last modified the field', on_delete=django.db.models.deletion.PROTECT, related_name='risk_projectprogress_related_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Project Progress',
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='rag',
        ),
        migrations.RemoveField(
            model_name='projectupdate',
            name='indicator',
        ),
        migrations.AddField(
            model_name='projectmilestone',
            name='rag',
            field=models.ForeignKey(default=1, help_text='RAG indicator of the milestone', on_delete=django.db.models.deletion.PROTECT, related_name='projectmilestone_rag', to='risk.RAGIndicator'),
        ),
        migrations.AddField(
            model_name='projectupdate',
            name='rag',
            field=models.ForeignKey(default=1, help_text='RAG indicator of the project', on_delete=django.db.models.deletion.PROTECT, related_name='project_rag', to='risk.RAGIndicator'),
        ),
        migrations.AddField(
            model_name='projectprogress',
            name='project',
            field=models.ForeignKey(help_text='Project the milestone is associated', on_delete=django.db.models.deletion.PROTECT, related_name='project_progress', to='risk.Project'),
        ),
        migrations.AddField(
            model_name='projectnextstep',
            name='project',
            field=models.ForeignKey(help_text='Project the milestone is associated', on_delete=django.db.models.deletion.PROTECT, related_name='project_nextstep', to='risk.Project'),
        ),
    ]
