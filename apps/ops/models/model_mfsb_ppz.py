from django.db import models


class MfsbPpz(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=150, blank=True, null=True)
    code = models.IntegerField(db_column='Code', blank=True, null=True)
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    check = models.BooleanField(db_column='Check')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ppz'

