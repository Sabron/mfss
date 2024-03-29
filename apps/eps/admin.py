from django.contrib import admin

from .models.model_tags import Tag
from .models.model_tagdates import TagDate
from .models.model_anchors import Anchors

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('sn','name','le_status')
    search_fields = ('sn',)

@admin.register(TagDate)
class TagDateAdmin(admin.ModelAdmin):
    list_display = ('tag','time','le_status')
    search_fields = ('sensor__sn',)

@admin.register(Anchors)
class AnchorsAdmin(admin.ModelAdmin):
    list_display = ('label','sn','disabled','subscribed')
    search_fields = ('label',)