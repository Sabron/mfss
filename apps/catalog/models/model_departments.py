# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns


class Department(models.Model):  # Подразделения клиента
    """
    Модель справочника зон доступа
    """

    name = models.CharField(max_length=60, help_text="",default=" ",verbose_name="Наименование")
    comments=models.TextField(max_length=1000, blank=True, verbose_name="Комментарий",default=' ')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    class Meta:   # отображение в админики
        ordering = ['name']
        verbose_name = u'подразделение'
        verbose_name_plural = u'подразделения'
        indexes = [
            models.Index(fields=['name']),
            ]
