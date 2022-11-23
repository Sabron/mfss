# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.model_zones import Zone
from .models.model_locations import Location
from .models.model_positions import Position
from .models.model_departments  import Department
from .models.model_workers import Worker

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ['name']
    search_fields = ('name',)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name','id','tabnomer', 'sex_workers','department','position','phone')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin): #Подразделения
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin): #объекты
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin): #Зоны
    ordering = ('name',)
    list_display = ('location','name')
    list_filter = ('location',)
