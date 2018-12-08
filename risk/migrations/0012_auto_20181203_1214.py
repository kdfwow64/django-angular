# Generated by Django 2.1.3 on 2018-12-03 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0011_auto_20181203_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='about',
            field=models.TextField(blank=True, help_text='Information about the vendor from their website', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email_info',
            field=models.EmailField(blank=True, help_text='Addtional information email address for the vendor.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email_product',
            field=models.EmailField(blank=True, help_text='For internal use to get information from the vendor regarding products and services', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone_info',
            field=models.CharField(blank=True, help_text='Vendor information phone number', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone_support',
            field=models.CharField(blank=True, help_text='Vendor support phone number', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='url_main',
            field=models.URLField(blank=True, help_text='Vendors main website', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='url_product',
            field=models.URLField(blank=True, help_text='Vendors products website', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='url_service',
            field=models.URLField(blank=True, help_text='Vendors services website', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='url_support',
            field=models.URLField(blank=True, help_text='Vendors support website', null=True),
        ),
    ]
