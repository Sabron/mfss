# Generated by Django 2.2.4 on 2022-11-23 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20221025_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='TimeZone',
        ),
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
    ]
