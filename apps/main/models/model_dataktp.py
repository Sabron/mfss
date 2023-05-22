from django.db import models


class DataKtp(models.Model):
    date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время значения")
    name = models.CharField(
        max_length=160,
        default=" ",
        blank=True,
        null=True,
        verbose_name="ТЭГ") 
    values = models.CharField(
        max_length=50,
        default=" ",
        blank=True,
        null=True,
        verbose_name="Значение")
    check = models.BooleanField(
        blank=True,
        default=True,
        verbose_name="Активная отметка")

    class Meta:
        unique_together = ('name', 'date')
        verbose_name = u'показатель КТП'
        verbose_name_plural = u'показатели КТП'
        indexes = [
            models.Index(fields=['date','name',]),
            models.Index(fields=['name',]),
            models.Index(fields=['name','check']),
            ]
