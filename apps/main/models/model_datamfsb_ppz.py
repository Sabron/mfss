from django.db import models


class DataMfsbPpz(models.Model): # Противопожарной защиты
    date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        verbose_name="Время значения")
    name = models.CharField(
        max_length=450,
        default=" ",
        blank=True,
        null=True,
        verbose_name="ТЭГ") 
    code = models.IntegerField(default=1,
                              help_text="",
                              blank=True,
                              verbose_name="Код")
    check = models.BooleanField(
        blank=True,
        default=True,
        verbose_name="Активная отметка")

    class Meta:
        unique_together = ('name', 'date')
        verbose_name = u'показатель противопожарной защиты'
        verbose_name_plural = u'показатель противопожарной защиты'
        indexes = [
            models.Index(fields=['date','name',]),
            models.Index(fields=['name',]),
            ]


