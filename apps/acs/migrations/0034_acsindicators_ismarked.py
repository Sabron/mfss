# Generated by Django 2.2 on 2023-03-02 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0033_auto_20230228_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='acsindicators',
            name='ismarked',
            field=models.BooleanField(blank=True, default=False, verbose_name='Пометка'),
        ),
    ]
