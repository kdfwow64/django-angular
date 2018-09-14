# Generated by Django 2.0.5 on 2018-08-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0026_auto_20180730_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, help_text='The profile image and location for the user', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='providence_code',
            field=models.CharField(blank=True, help_text='Select state or providence', max_length=30, null=True),
        ),
    ]