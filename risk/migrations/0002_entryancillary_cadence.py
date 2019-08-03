# Generated by Django 2.1.3 on 2019-06-21 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entryancillary',
            name='cadence',
            field=models.CharField(choices=[('R', 'Re-occuring'), ('O', 'Once')], default='O', help_text='Will the ancillary item have a continuous afffect', max_length=1),
        ),
    ]
