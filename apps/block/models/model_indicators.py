# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from .model_sensor import BlockSensor

class BlockIndicators(models.Model):  # Показания блокировок
    type_list = (
        (0, 'нет связи (блокировка выведена)'),
        (1, 'блокировка активна'),
    )
     
    date_time = models.DateTimeField(auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время показаний")
    sensor = models.ForeignKey(BlockSensor,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Датчик")
    value = models.IntegerField(choices=type_list,
           blank=True,
           default=0,
           verbose_name="Активность") 
    

    def getId(self):
        return self.id

    def __str__(self):
        return self.sensor.name

    class Meta:   # отображение в админики
        ordering = ('sensor',)
        verbose_name = u'показание датчика'
        verbose_name_plural = u'показания датчиков'
        indexes = [
            models.Index(fields=['date_time','sensor',]),]




