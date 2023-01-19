from django.contrib import admin

from .models.model_sensor import ScadaSensor
from .models.model_indicators import ScadaIndicators

@admin.register(ScadaSensor)
class ScadaSensorAdmin(admin.ModelAdmin):
    list_display = ('zone','tag','name','value','active')
    search_fields = ('name',)

@admin.register(ScadaIndicators)
class ScadaIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','value')
    search_fields = ('sensor__name',)
