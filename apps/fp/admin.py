from django.contrib import admin

from .models.model_code_bolid import CodeBolid


@admin.register(CodeBolid)
class CodeBolidAdmin(admin.ModelAdmin):
    list_display = ('code','name')
    search_fields = ('name',)
