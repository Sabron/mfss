# Generated by Django 2.2.4 on 2023-02-11 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0026_auto_20230211_1318'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='acsindicators',
            name='acs_acsindi_type_d3dab2_idx',
        ),
        migrations.RemoveField(
            model_name='acsindicators',
            name='type',
        ),
        migrations.AddField(
            model_name='acssensor',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, 'Не определен'), (1, 'Датчик диоксида углерода (CO2)'), (2, 'Датчик оксида (CO) '), (3, 'Датчик метана (CH4)')], default=0, verbose_name='Тип датчика'),
        ),
        migrations.AddIndex(
            model_name='acssensor',
            index=models.Index(fields=['type'], name='acs_acssens_type_d48038_idx'),
        ),
    ]
