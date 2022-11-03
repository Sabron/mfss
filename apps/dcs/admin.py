from django.contrib import admin

from .models.model_sensor import DcsSensor
from .models.model_indicators import DcsIndicators

@admin.register(DcsSensor)
class DcsSensorAdmin(admin.ModelAdmin):
    list_display = ('tag','name','connect_time','critical_value','ratio','max_value','critical_type','active')
    search_fields = ('name',)

@admin.register(DcsIndicators)
class DcsIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','value')
    search_fields = ('sensor__name',)
