# Generated by Django 2.2.4 on 2022-10-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagdate',
            name='accuracy',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tagdate',
            name='kinematic',
            field=models.IntegerField(default=0),
        ),
    ]
