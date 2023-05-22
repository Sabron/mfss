# Generated by Django 2.2 on 2023-05-23 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ktp', '0006_remove_ktpindicators_ismarked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ktpindicators',
            name='value_akt',
            field=models.BigIntegerField(default=0, verbose_name='Активная ЭЭ'),
        ),
        migrations.AlterField(
            model_name='ktpindicators',
            name='value_reakt',
            field=models.BigIntegerField(default=0, verbose_name='Реактивная ЭЭ'),
        ),
    ]
