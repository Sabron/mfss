# Generated by Django 2.2 on 2022-10-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0015_auto_20221024_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='acssensor',
            name='step',
            field=models.FloatField(blank=True, default=0.01, verbose_name='Показание'),
        ),
    ]
