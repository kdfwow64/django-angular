# Generated by Django 2.0.5 on 2018-10-17 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0054_auto_20181017_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companymemberrole',
            name='desc',
            field=models.TextField(blank=True, help_text='Description of the role', null=True),
        ),
    ]
