# Generated by Django 2.2.4 on 2023-01-19 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeBolid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(blank=True, default=1, verbose_name='Код БОЛИД')),
                ('name', models.CharField(default=' ', max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Код БОЛИД',
                'verbose_name_plural': 'Код БОЛИД',
                'ordering': ('name',),
            },
        ),
        migrations.AddIndex(
            model_name='codebolid',
            index=models.Index(fields=['code'], name='fp_codeboli_code_a9cdb4_idx'),
        ),
    ]
