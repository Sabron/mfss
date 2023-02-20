# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

from apps.catalog.models.model_zones import Zone

class AcsSensor(models.Model):  # Датчики
    critical_type_list = (('max', 'Максимальный'),
        ('min', 'Минимальный'),)
   
    type_list = (
        (0, '< Не определен >'),
        (1, 'Датчик диоксида углерода (CO2)'),
        (2, 'Датчик оксида (CO)'),
        (3, 'Датчик метана (CH4)'),
    )

    """
    Модель справочника датчиков
    """
    zone = models.ForeignKey(Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Зона")
    type = models.IntegerField(choices=type_list,
           blank=True,
           default=0,
           verbose_name="Тип датчика") 
    tag = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="ТЭГ")
    name = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="Наименование")
    critical_value = models.FloatField(default=0.0,
        help_text="",
        verbose_name="Критически допустимое значение")
    critical_type = models.CharField(max_length=3,
        verbose_name = "Тип",
        choices = critical_type_list,
        default=1)
    active = models.BooleanField(verbose_name=u'Активный',
        null=False,
        default=True,
        blank=True)
    ratio = models.IntegerField(default=1,
                              help_text="",
                              blank=True,
                              verbose_name="Масштабирование")
    value = models.FloatField(default=0.0,
                              help_text="",
                              blank=True,
                              verbose_name="Показание")
    max_value = models.FloatField(default=0.0,
        help_text="",
        blank=True,
        verbose_name="Максимальное значение")
    unit = models.CharField(max_length=10,
        help_text="",
        default=" ",
        verbose_name="Ед.измерения")
    comments = models.TextField(max_length=1001,
        blank=True,
        verbose_name="Комментарий",default=' ')
    scale = models.CharField(max_length=250,
        help_text="",
        default="0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0",
        verbose_name="Шкала датчика")
    norm_value_from = models.FloatField(default=0.0,
        help_text="",
        verbose_name="Показатель нормы от")
    norm_value_to = models.FloatField(default=0.0,
        help_text="",
        verbose_name="Показатель нормы до")
    danger_value_from = models.FloatField(default=0.0,
        help_text="",
        verbose_name="Показатель опасности от")
    danger_value_to = models.FloatField(default=0.0,
        help_text="Показатель опасности до",
        verbose_name="Показатель опасности до")
    critical_value_from = models.FloatField(default=0.0,
        help_text="",
        verbose_name="Критический показатель от")
    critical_value_to = models.FloatField(default=0.0,
        help_text="",
        verbose_name="Критический показатель до")
    connect_time = models.DateTimeField(
        default=datetime.now,
        blank=True,
        verbose_name="Последнее подключение")
     

    def getId(self):
        return self.id

    def __str__(self):
        return self.name+' ( '+str(self.id)+' )'

    class Meta:   # отображение в админики
        ordering = ('name',)
        verbose_name = u'датчик'
        verbose_name_plural = u'датчики'
        indexes = [models.Index(fields=['tag',]),
            models.Index(fields=['name',]),
            models.Index(fields=['type',]),
            models.Index(fields=['tag','name',]),]


