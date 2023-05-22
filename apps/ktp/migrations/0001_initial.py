# Generated by Django 2.2 on 2023-05-22 23:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0008_auto_20230323_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='KtpSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default=' ', max_length=160, verbose_name='ТЭГ')),
                ('name', models.CharField(default=' ', max_length=160, verbose_name='Наименование')),
                ('serial', models.CharField(default=' ', max_length=5, verbose_name='Серийный номер')),
                ('connect_time', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Последнее подключение')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Zone', verbose_name='Зона')),
            ],
            options={
                'verbose_name': 'датчик',
                'verbose_name_plural': 'датчики',
                'ordering': ('name',),
            },
        ),
        migrations.AddIndex(
            model_name='ktpsensor',
            index=models.Index(fields=['tag'], name='ktp_ktpsens_tag_e0fc3a_idx'),
        ),
        migrations.AddIndex(
            model_name='ktpsensor',
            index=models.Index(fields=['name'], name='ktp_ktpsens_name_06bea3_idx'),
        ),
        migrations.AddIndex(
            model_name='ktpsensor',
            index=models.Index(fields=['tag', 'name'], name='ktp_ktpsens_tag_1c40a5_idx'),
        ),
    ]
