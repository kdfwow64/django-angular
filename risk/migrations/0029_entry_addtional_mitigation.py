# Generated by Django 2.0.5 on 2018-09-06 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0028_auto_20180906_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='addtional_mitigation',
            field=models.TextField(blank=True, help_text='Used to provide context on additional mitigation thoughts from the contributor', null=True),
        ),
    ]