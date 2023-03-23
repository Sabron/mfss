# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.contenttypes.models import ContentType

class Settings(models.Model):  # Настройки 
    name = models.CharField(max_length=20, help_text="",verbose_name="Наименование")
    value = models.CharField(max_length=100, blank=True,help_text="",verbose_name="Значение")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    class Meta:   # отображение в админики
        unique_together = ['name']
        ordering = ['name']
        verbose_name = u'настройка '
        verbose_name_plural = u'настройки'
    
    




