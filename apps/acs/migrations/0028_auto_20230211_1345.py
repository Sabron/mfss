# Generated by Django 2.2.4 on 2023-02-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0027_auto_20230211_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acssensor',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, '< Не определен >'), (1, 'Датчик диоксида углерода (CO2)'), (2, 'Датчик оксида (CO)'), (3, 'Датчик метана (CH4)')], default=0, verbose_name='Тип датчика'),
        ),
    ]
