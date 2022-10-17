# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns


class PositionsManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Positions(models.Model):  # Должности клиента
    """
    Модель справочника должности
    """

    name = models.CharField(max_length=60, help_text="",default=" ",verbose_name="Наименование")
    
    objects=PositionsManager()


    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    def get_natural_key(self):
        return [self.name]

    #def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
       # return reverse('positions_update', args=[str(self.id)])

    def __unicode__(self):
        return self.name
    class Meta:   # отображение в админики
        ordering = ['name']
        verbose_name = u'должность'
        verbose_name_plural = u'должности'
        indexes = [
            models.Index(fields=['name']),
            ]

