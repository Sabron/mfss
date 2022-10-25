# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from .model_tags import Tag

class TagDate(models.Model):  # Отметки
    """
    Модель отметок датчика
    """
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Датчик")
    time = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время отметки")
    accuracy = models.IntegerField(default=0)
    kinematic = models.IntegerField(default=0)
    seq = models.IntegerField(default=0)
    source = models.CharField(
        max_length=60,
        help_text="",
        default=" ",
        verbose_name="source")
    le_status = models.CharField(
        max_length=60,
        help_text="",
        default=" ",
        verbose_name="Статус")
    motion = models.CharField(
        max_length=60,
        help_text="",
        default=" ",
        verbose_name="motion")
    solution = models.CharField(
        max_length=60,
        help_text="",
        default=" ",
        verbose_name="solution")
    x = models.FloatField(default=0.0,
        help_text="",
        verbose_name="x")
    y = models.FloatField(default=0.0,
        help_text="",
        verbose_name="y")
    z = models.FloatField(default=0.0,
        help_text="",
        verbose_name="z")
    
    class Meta:   # отображение в админики
        unique_together = ('tag','time',)
        verbose_name = u'отметка'
        verbose_name_plural = u'отметки'
        indexes = [
            models.Index(fields=['tag',]),
            ]


