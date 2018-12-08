# Generated by Django 2.1.3 on 2018-12-03 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0009_auto_20181202_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='initial_account',
            field=models.ForeignKey(default=1, help_text='Account that initally created the vendor', on_delete=django.db.models.deletion.PROTECT, related_name='inital_account_vendor', to='risk.Account'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='notes_mgmt',
            field=models.TextField(blank=True, help_text='Management notes regarding the vendor', null=True),
        ),
    ]
