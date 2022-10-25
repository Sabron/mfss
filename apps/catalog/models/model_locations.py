# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns



class Location(models.Model):  # Объекты
    time_zone_list = (
        (2, 'UTC+02 (Калининградское время)'),
        (3, 'UTC+03 (Московское время)'),
        (4, 'UTC+04 (Самарское время)'),
        (5, 'UTC+05 (Екатеринбургское время)'),
        (6, 'UTC+06 (Омское время)'),
        (7, 'UTC+07 (Красноярское время)'),
        (8, 'UTC+08 (Иркутское время)'),
        (9, 'UTC+09 (Якутское время)'),
        (10, 'UTC+10 (Владивостокское время)'),
        (11, 'UTC+11 (Среднеколымское время)'),
        (12, 'UTC+12 (Камчатское время)'),
    )
    
    """
    Модель справочника объекты
    """
    name = models.CharField(max_length=60, help_text="",default=" ",verbose_name="Наименование")
    TimeZone= models.IntegerField(choices=time_zone_list,default=3,verbose_name="Часовой пояс")
    latitude = models.CharField(max_length=60,default=' ', blank=True,help_text="",verbose_name="Широта")
    longitude = models.CharField(max_length=60,default=' ', blank=True,help_text="",verbose_name="Долгота")


    
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
