# Generated by Django 2.2.4 on 2023-02-28 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fp', '0003_auto_20230119_2130'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='fpindicators',
            name='fp_fpindica_sensor__0c7f88_idx',
        ),
    ]
