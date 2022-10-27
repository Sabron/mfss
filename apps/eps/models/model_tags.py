# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

class Tag(models.Model):  # Датчики
    critical_type_list = (('max', 'Максимальный'),
        ('min', 'Минимальный'),)

    """
    Модель справочника датчиков
    """
    name = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="Наименование")
    sn = models.CharField(max_length=60,
        help_text="",
        default=" ",
        verbose_name="Серийный номер")
    descr = models.CharField(max_length=100,
        help_text="",
        default=" ",
        verbose_name="descr")
    origin = models.CharField(max_length=100,
        help_text="",
        default=" ",
        verbose_name="origin")
    le_status = models.CharField(
        max_length=60,
        help_text="",
        default=" ",
        verbose_name="Статус")
    x = models.FloatField(default=0.0,
        help_text="",
        verbose_name="x")
    y = models.FloatField(default=0.0,
        help_text="",
        verbose_name="y")
    z = models.FloatField(default=0.0,
        help_text="",
        verbose_name="z")
  
    def getId(self):
        return self.id

    def __str__(self):
        return self.name

    class Meta:   # отображение в админики
        ordering = ('name',)
        verbose_name = u'датчик'
        verbose_name_plural = u'датчики'
        indexes = [models.Index(fields=['name',]),
            ]


