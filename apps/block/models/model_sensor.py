# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

from apps.catalog.models.model_zones import Zone

class BlockSensor(models.Model):  
    type_list = (
        (0, 'нет связи (блокировка выведена)'),
        (1, 'блокировка активна'),
    )

    zone = models.ForeignKey(Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Зона")
    tag = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="ТЭГ")
    position = models.CharField(max_length=20,
        help_text="",
        default=" ",
        blank = True,
        verbose_name="Позиция")
    name = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="Наименование")
    value = models.IntegerField(choices=type_list,
           blank=True,
           default=0,
           verbose_name="Активность") 
    connect_time = models.DateTimeField(
        default=datetime.now,
        blank=True,
        verbose_name="Последнее подключение")
     

    def getId(self):
        return self.id

    def __str__(self):
        return self.name

    class Meta:   # отображение в админики
        ordering = ('name',)
        verbose_name = u'датчик блокировки'
        verbose_name_plural = u'датчики блокировок'
        indexes = [models.Index(fields=['tag',]),
            models.Index(fields=['name',]),
            models.Index(fields=['tag','name',]),]



