# Generated by Django 2.1.3 on 2019-04-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0018_auto_20190426_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='entryancillary',
            name='cost_detail',
            field=models.TextField(blank=True, help_text='Information regarding the elements used to determine the ancillary cost', null=True),
        ),
        migrations.AddField(
            model_name='entryancillary',
            name='per_occurance',
            field=models.BooleanField(default=False, help_text='Defines if an ancillary cost is based on a quantity of occurences'),
        ),
        migrations.AlterField(
            model_name='entryancillary',
            name='evaluation_flg',
            field=models.BooleanField(default=False, help_text='Defines if an evaluation is due for the ancillary cost'),
        ),
    ]
