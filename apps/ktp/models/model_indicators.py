# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from .model_sensor import KtpSensor

class KtpIndicators(models.Model):  # Показания датчиков
  
    
    """
    Модель справочника датчиков
    """
    date_time = models.DateTimeField(auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время показаний")
    sensor = models.ForeignKey(KtpSensor,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Датчик")
    value_akt = models.BigIntegerField(default=0,
         verbose_name="Активная ЭЭ")
    value_reakt = models.BigIntegerField(default=0,
         verbose_name="Реактивная ЭЭ")

    def getId(self):
        return self.id

    def __str__(self):
        return self.sensor.name

    class Meta:   # отображение в админики
        ordering = ('sensor',)
        verbose_name = u'показание датчика'
        verbose_name_plural = u'показания датчиков'
        indexes = [
            models.Index(fields=['sensor','date_time',]),
            #models.Index(fields=['date_time',]),
            
            ]



