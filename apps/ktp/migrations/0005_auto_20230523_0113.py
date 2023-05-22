# Generated by Django 2.2 on 2023-05-23 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ktp', '0004_ktpsensor_serial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ktpindicators',
            name='value',
        ),
        migrations.AddField(
            model_name='ktpindicators',
            name='value_akt',
            field=models.BigIntegerField(default=0, verbose_name='Активной ЭЭ'),
        ),
        migrations.AddField(
            model_name='ktpindicators',
            name='value_reakt',
            field=models.BigIntegerField(default=0, verbose_name='Реактивной ЭЭ'),
        ),
    ]
