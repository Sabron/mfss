from django.contrib import admin
from apps.main.models.model_datamfsb import DataMfsb

@admin.register(DataMfsb)
class DataMfsbAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)
