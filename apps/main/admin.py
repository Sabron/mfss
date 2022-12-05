from django.contrib import admin
from apps.main.models.model_datamfsb import DataMfsb
from apps.main.models.model_datamfsb_skada import DataMfsbSkada

@admin.register(DataMfsb)
class DataMfsbAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)

@admin.register(DataMfsbSkada)
class DataMfsbSkadaAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)
