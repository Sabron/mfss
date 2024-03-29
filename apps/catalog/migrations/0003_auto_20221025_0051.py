# Generated by Django 2.2 on 2022-10-25 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20221025_0049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=' ', max_length=60, verbose_name='Наименование')),
                ('comments', models.TextField(blank=True, default=' ', max_length=1000, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'подразделение',
                'verbose_name_plural': 'подразделения',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=' ', max_length=60, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'должность',
                'verbose_name_plural': 'должности',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabnomer', models.CharField(blank=True, help_text='Табельный номер', max_length=10, verbose_name='Таб.№')),
                ('name', models.CharField(db_index=True, default=' ', max_length=160, verbose_name='ФИО')),
                ('lastName', models.CharField(db_index=True, max_length=60, verbose_name='Фамилия')),
                ('firstName', models.CharField(db_index=True, max_length=50, verbose_name='Имя')),
                ('otchestvo', models.CharField(blank=True, default=' ', max_length=60, verbose_name='Отчество')),
                ('sex_workers', models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')], default='m', max_length=1, verbose_name='Пол')),
                ('phone', models.CharField(blank=True, max_length=18, verbose_name='Телефон')),
                ('Comments', models.TextField(blank=True, default=' ', max_length=1000, verbose_name='Комментарий')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Department', verbose_name='Подразделение')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'сотрудник',
                'verbose_name_plural': 'сотрудники',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='position',
            index=models.Index(fields=['name'], name='catalog_pos_name_e93e3a_idx'),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['name'], name='catalog_dep_name_7addcd_idx'),
        ),
        migrations.AddIndex(
            model_name='worker',
            index=models.Index(fields=['name'], name='catalog_wor_name_210f0d_idx'),
        ),
    ]
