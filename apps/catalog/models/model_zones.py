# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from .model_locations import Location


class Zone(models.Model):  # Зоны
    """
    Модель справочника зон доступа
    """

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,verbose_name="Объект")
    name = models.CharField(max_length=60, help_text="",default=" ",verbose_name="Наименование")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.location)+'/'+self.name

    class Meta:   # отображение в админики
		#unique_together = ('client','location','name',) # уникальный ключ
        ordering = ('name',)
        verbose_name = u'зона'
        verbose_name_plural = u'зоны'
        indexes = [
            models.Index(fields=['location']),
            ]
