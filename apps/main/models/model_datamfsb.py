from django.db import models


class DataMfsb(models.Model):
    date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время значения")
    name = models.CharField(
        max_length=150,
        default=" ",
        blank=True,
        null=True,
        verbose_name="ТЭГ") 
    values = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Значение")
    check = models.BooleanField(
        blank=True,
        default=True,
        verbose_name="Активная отметка")

    class Meta:
        unique_together = ('name', 'date')
        verbose_name = u'показатель датчика АГК И и КЗ'
        verbose_name_plural = u'показатели датчиков АГК И и КЗ'
        indexes = [
            models.Index(fields=['date','name',]),
            models.Index(fields=['name',]),
            models.Index(fields=['name','check']),
            ]
