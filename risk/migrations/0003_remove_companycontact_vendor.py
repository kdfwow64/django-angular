# Generated by Django 2.0.5 on 2018-05-27 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0002_auto_20180526_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companycontact',
            name='vendor',
        ),
    ]
