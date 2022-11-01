# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

class Anchors(models.Model):  # Анкера
    """
    Модель справочника Анкеров
    """
    rls_id = models.CharField(max_length=160,
        help_text="",
        default=" ",
        verbose_name="id rls")
    sn = models.CharField(max_length=60,
        help_text="",
        default=" ",
        verbose_name="Серийный номер")
    origin = models.CharField(max_length=100,
        help_text="",
        default=" ",
        verbose_name="origin")
    disabled = models.BooleanField(blank=False,
                                   default=False,
                                   verbose_name="disabled")
    descr = models.CharField(max_length=100,
        help_text="",
        default=" ",
        verbose_name="descr")
    label = models.CharField(max_length=100,
        help_text="",
        default=" ",
        verbose_name="label")
    x = models.FloatField(default=0.0,
        help_text="",
        verbose_name="x")
    y = models.FloatField(default=0.0,
        help_text="",
        verbose_name="y")
    z = models.FloatField(default=0.0,
        help_text="",
        verbose_name="z")
    device_type = models.CharField(max_length=50,
        help_text="",
        default=" ",
        verbose_name="device_type")
    status = models.CharField(max_length=20,
        help_text="",
        default=" ",
        verbose_name="status")
    ip_address = models.CharField(max_length=20,
        help_text="",
        default=" ",
        verbose_name="ip_address")
    coap_resource = models.CharField(max_length=20,
        help_text="",
        default=" ",
        verbose_name="coap_resource")
    subscribed = models.BooleanField(blank=False,
                                   default=False,
                                   verbose_name="subscribed")
    message_time = models.DateTimeField(auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="message_time")
    status_time = models.DateTimeField(auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="status_time")
    total_packets = models.IntegerField(default=0)
    invalid_packets = models.IntegerField(default=0)
  
    def getId(self):
        return self.id

    def __str__(self):
        return self.label

    class Meta:   # отображение в админики
        ordering = ('label',)
        verbose_name = u'анкер'
        verbose_name_plural = u'анкера'
        indexes = [models.Index(fields=['label',]),]


