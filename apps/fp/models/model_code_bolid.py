# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models

class CodeBolid(models.Model):  # Справочник кодов БОЛИД
    """
    Справочник кодов БОЛИД
    """
    code = models.IntegerField(default=1,
                              help_text="",
                              blank=True,
                              verbose_name="Код БОЛИД")
    name = models.CharField(max_length=200,
        help_text="",
        default=" ",
        verbose_name="Наименование")

    def getId(self):
        return self.id

    def __str__(self):
        return self.name

    class Meta:   # отображение в админики
        ordering = ('name',)
        verbose_name = u'Код БОЛИД'
        verbose_name_plural = u'Коды БОЛИД'
        indexes = [models.Index(fields=['code',]),]



