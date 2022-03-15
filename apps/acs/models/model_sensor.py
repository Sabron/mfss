# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class AcsSensor(models.Model):  # Датчики
    critical_type_list = (
        ('max', 'Максимальный'),
        ('min', 'Минимальный'),
    )

    """
    Модель справочника датчиков
    """
    name = models.CharField(
        max_length=60,
        help_text="",
        default=" ",
        verbose_name="Наименование")
    critical_value = models.IntegerField(
        default=0,
        help_text="",
        verbose_name="Критически допустимое значение")
    critical_type = models.CharField(
        max_length=3,
        verbose_name = "Тип",
        choices = critical_type_list,
        default=1)
    active = models.BooleanField(
        verbose_name=u'Активный',
        null=False,
        default=True,
        blank=True)
    value = models.IntegerField(
        default=0,
        help_text="",
        verbose_name="Показание")
    comments = models.TextField(
        max_length=1001,
        blank=True,
        verbose_name="Комментарий",default=' ')
        

    def getId(self):
        return self.id

    def __str__(self):
        return self.name

    class Meta:   # отображение в админики
        ordering = ('name',)
        verbose_name = u'датчик'
        verbose_name_plural = u'датчики'
        indexes = [
            models.Index(fields=['name',]),
            ]


