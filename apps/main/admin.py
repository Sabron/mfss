from django.contrib import admin

from apps.main.models.model_datamfsb import DataMfsb
from apps.main.models.model_datamfsb_skada import DataMfsbSkada
from apps.main.models.model_datamfsb_ppz import DataMfsbPpz
from apps.main.models.model_datamfsb_skpv import DataMfsbSkpv
from apps.main.models.model_dataktp import DataKtp

@admin.register(DataMfsb)
class DataMfsbAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)

@admin.register(DataKtp)
class DataKtpAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)


@admin.register(DataMfsbSkada)
class DataMfsbSkadaAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)

@admin.register(DataMfsbPpz)
class DataMfsbPpzAdmin(admin.ModelAdmin):
    list_display = ('date','name','code')
    search_fields = ('name',)

@admin.register(DataMfsbSkpv)
class DataMfsbSkpvAdmin(admin.ModelAdmin):
    list_display = ('date','name','values','check')
    search_fields = ('name',)

