# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from .model_departments import Department
from .model_positions import Positions



class Workers(models.Model):  # Сотрудники
    sex_workers_list = (('m', 'Мужской'),
        ('f', 'Женский'),)

    """
    Модель справочника сотрудники
    """
    tabnomer = models.CharField(max_length=10,
                               blank=True,
                               help_text="Табельный номер",
                               verbose_name="Таб.№")
    name = models.CharField(max_length=160,
                           help_text="",
                           default=" ",
                           verbose_name="ФИО",
                           db_index=True)
    lastName = models.CharField(max_length=60,
                               help_text="",
                               verbose_name="Фамилия",
                               db_index=True)
    firstName = models.CharField(max_length=50,
                                 help_text="",
                                 verbose_name="Имя",
                                 db_index=True)
    otchestvo = models.CharField(max_length=60,
                                 blank=True,
                                 default=' ',
                                 help_text="",
                                 verbose_name="Отчество")
    sex_workers = models.CharField(max_length=1,
                                   choices=sex_workers_list,
                                   blank=False,
                                   default='m',
                                   verbose_name="Пол")
    department = models.ForeignKey(Department,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   help_text="",
                                   verbose_name="Подразделение")
    position = models.ForeignKey(Positions,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 help_text="",
                                 verbose_name="Должность")
    phone = models.CharField(max_length=18,
                           help_text="",
                           verbose_name="Телефон",
                           blank=True)
    Comments = models.TextField(max_length=1000,
                              default=' ',
                              blank=True,
                              verbose_name="Комментарий")
    def __str__(self):
        return '%s %s %s' % (self.lastName,self.firstName,self.otchestvo)
    class Meta:   # отображение в админики
        #unique_together = ('client', 'idclient')
        ordering = ['name']
        verbose_name = u'сотрудник'
        verbose_name_plural = u'сотрудники'
        indexes = [models.Index(fields=['name',]),]

