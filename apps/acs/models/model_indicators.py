# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from .model_sensor import AcsSensor

class AcsIndicators(models.Model):  # Показания датчиков
    """
    Модель справочника датчиков
    """
    date_time = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время показаний")
    sensor = models.ForeignKey(
        AcsSensor,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Датчики")
    value = models.IntegerField(
        default=0,
        help_text="",
        verbose_name="Показание")

    def getId(self):
        return self.id

    def __str__(self):
        return self.sensor.name

    class Meta:   # отображение в админики
        ordering = ('sensor',)
        verbose_name = u'показание датчика'
        verbose_name_plural = u'показания датчиков'
        indexes = [
            models.Index(fields=['date_time','sensor',]),
            ]



