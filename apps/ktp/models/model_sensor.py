# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

from apps.catalog.models.model_zones import Zone

class KtpSensor(models.Model):  # Датчики

    """
    Модель справочника датчиков
    """
    zone = models.ForeignKey(Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Зона")
    tag = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="ТЭГ")
    name = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="Наименование")
    serial = models.CharField(max_length=5,
        help_text="",
        default=" ",
        verbose_name="Серийный номер")
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
        verbose_name = u'датчик'
        verbose_name_plural = u'датчики'
        indexes = [
            models.Index(fields=['tag',]),
            models.Index(fields=['name',]),
            models.Index(fields=['tag','name',]),]



