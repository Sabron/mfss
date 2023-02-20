from django.db import models


class MfsbBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    values = models.FloatField(db_column='Values', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    check = models.BooleanField(db_column='Check')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'block'
