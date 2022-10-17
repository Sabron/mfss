# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.model_positions import Positions
from .models.model_departments  import Department
from .models.model_workers import Workers

@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ['name']
    search_fields = ('name',)

@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ('name','id','tabnomer', 'sex_workers','department','position','phone')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin): #Подразделения
    list_display = ('name',)
    search_fields = ('name',)
    
