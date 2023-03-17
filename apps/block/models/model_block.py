from django.db import models


class Block(models.Model):
    name = models.CharField(db_column='Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    values = models.FloatField(db_column='Values', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    check = models.BooleanField(db_column='Check', blank=True, null=True,default=False)  # Field name made lowercase.

    class Meta:
        verbose_name = u'Блокировки'
        

