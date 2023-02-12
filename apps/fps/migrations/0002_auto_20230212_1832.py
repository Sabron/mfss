# Generated by Django 2.2.4 on 2023-02-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fpssensor',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, '< Не определен >'), (1, 'Датчик'), (2, 'Емкость')], default=0, verbose_name='Тип датчика'),
        ),
        migrations.AddIndex(
            model_name='fpssensor',
            index=models.Index(fields=['type'], name='fps_fpssens_type_086d77_idx'),
        ),
    ]
