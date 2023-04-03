# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns



class Location(models.Model):  # Объекты
   
    """
    Модель справочника объекты
    """
    name = models.CharField(max_length=60,
                           help_text="",
                           default=" ",
                           verbose_name="Наименование")


    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    class Meta:   # отображение в админики
        ordering = ('name',)
        verbose_name = u'объект'
        verbose_name_plural = u'Объекты'
        indexes = [
            models.Index(fields=['name']),
            ]
