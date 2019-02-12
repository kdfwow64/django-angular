# Generated by Django 2.1.3 on 2019-02-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0042_auto_20190125_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrycompanyasset',
            name='exposure_factor',
        ),
        migrations.RemoveField(
            model_name='entrycompanycontrol',
            name='aro_mitigation_rate',
        ),
        migrations.RemoveField(
            model_name='entrycompanycontrol',
            name='impact_mitigation_rate',
        ),
        migrations.AddField(
            model_name='entrycompanycontrol',
            name='aro_mitigation_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Monetary amount of mitigation the control applies to the Annual Rate of Occurence', max_digits=30),
        ),
        migrations.AddField(
            model_name='entrycompanycontrol',
            name='impact_mitigation_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Monetary amount of mitigation the control applies to the Impact', max_digits=30),
        ),
    ]
