from django.contrib import admin

from .models.model_block import Block
from .models.model_sensor import BlockSensor
from .models.model_indicators import BlockIndicators

@admin.register(BlockSensor)
class BlockSensorAdmin(admin.ModelAdmin):
    list_display = ('name','zone','position','tag','connect_time','value')
    search_fields = ('name',)

@admin.register(BlockIndicators)
class BlockIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('date_time','sensor','value')
    search_fields = ('sensor__name',)

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name','values','date','check')
    search_fields = ('name',)
