from django.contrib import admin

from .models.model_code_bolid import CodeBolid
from .models.model_sensor import FpSensor
from .models.model_indicators import FpIndicators


@admin.register(CodeBolid)
class CodeBolidAdmin(admin.ModelAdmin):
    list_display = ('code','name')
    search_fields = ('name',)

@admin.register(FpSensor)
class FpSensorAdmin(admin.ModelAdmin):
    list_display = ('zone','tag','name','code','active')
    search_fields = ('name',)

@admin.register(FpIndicators)
class FpIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','code')
    search_fields = ('sensor__name',)
