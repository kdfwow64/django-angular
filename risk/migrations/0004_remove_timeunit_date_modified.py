# Generated by Django 2.0.5 on 2018-10-24 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0003_remove_timeunit_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeunit',
            name='date_modified',
        ),
    ]
