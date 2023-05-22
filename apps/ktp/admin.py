from django.contrib import admin

from .models.model_sensor import KtpSensor
from .models.model_indicators import KtpIndicators

@admin.register(KtpSensor)
class KtpSensorAdmin(admin.ModelAdmin):
    list_display = ('name','serial','zone','tag','connect_time')
    search_fields = ('name',)

@admin.register(KtpIndicators)
class KtpIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','value')
    search_fields = ('sensor__name',)
