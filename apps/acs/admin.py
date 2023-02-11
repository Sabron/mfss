from django.contrib import admin

from .models.model_sensor import AcsSensor
from .models.model_indicators import AcsIndicators

@admin.register(AcsSensor)
class AcsSensorAdmin(admin.ModelAdmin):
    list_display = ('name','type','active','zone','tag','connect_time','critical_value','ratio','max_value','critical_type')
    search_fields = ('name',)

@admin.register(AcsIndicators)
class AcsIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','value')
    search_fields = ('sensor__name',)
