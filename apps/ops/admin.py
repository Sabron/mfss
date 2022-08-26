from django.contrib import admin

from .models.model_mfsb import Mfsb
@admin.register(Mfsb)
class MfsbAdmin(admin.ModelAdmin):
    list_display = ('id','name','values','date','check')
    search_fields = ('name',)

