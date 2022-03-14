# -*- coding: utf-8 -*-
from django.contrib import admin


from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name','value')

