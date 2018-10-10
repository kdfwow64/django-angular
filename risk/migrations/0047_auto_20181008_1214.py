# Generated by Django 2.0.5 on 2018-10-08 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0046_auto_20181003_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrycompanyasset',
            name='asset_exposure_factor_toggle',
            field=models.IntegerField(choices=[(1, 'Percentage of Asset Value'), (2, 'Fixed Impact Value'), (3, 'Time Based Impact Value')], default=1, help_text='Toggle to determine which formula is used to determine the exposure factor'),
        ),
        migrations.AddField(
            model_name='entrycompanyasset',
            name='asset_exposure_factor_value',
            field=models.FloatField(blank=True, default=1, help_text='Maximum percentage of asset value exposed given the threat scenario', null=True),
        ),
        migrations.AddField(
            model_name='entrycompanyasset',
            name='fixed_exposure_factor_value',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The fixed monetary value of the exposure factor dollars', max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='entrycompanyasset',
            name='timed_exposure_factor_default',
            field=models.FloatField(blank=True, help_text='Default number of units used for calucalting the exposure factor', null=True),
        ),
        migrations.AddField(
            model_name='entrycompanyasset',
            name='timed_exposure_factor_unit',
            field=models.ForeignKey(default=3, help_text='Time units used to determine the exposure factor of the asset', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entrycompanyassetunits', to='risk.TimeUnit'),
        ),
        migrations.AddField(
            model_name='entrycompanyasset',
            name='timed_exposure_factor_value',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The monetary value of the exposure factor per unit in dollars', max_digits=30, null=True),
        ),
        migrations.AlterField(
            model_name='companycontrol',
            name='vendor_control',
            field=models.ForeignKey(blank=True, help_text='The primary control mapping for the company', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_companycontrol', to='risk.Control'),
        ),
    ]
