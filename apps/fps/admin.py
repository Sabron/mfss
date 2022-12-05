from django.contrib import admin

from .models.model_sensor import FpsSensor
from .models.model_indicators import FpsIndicators

@admin.register(FpsSensor)
class FpsSensorAdmin(admin.ModelAdmin):
    list_display = ('zone','tag','name','connect_time','critical_value','ratio','max_value','critical_type','active')
    search_fields = ('name',)

@admin.register(FpsIndicators)
class FpsIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','value')
    search_fields = ('sensor__name',)
