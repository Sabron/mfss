# Generated by Django 2.2 on 2022-12-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20221205_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamfsbskada',
            name='name',
            field=models.CharField(blank=True, default=' ', max_length=450, null=True, verbose_name='ТЭГ'),
        ),
    ]
