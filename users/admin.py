# -*- coding: utf-8 -*-
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class UserInline(admin.StackedInline):
    
    model = Profile
    can_delete = False
    verbose_name_plural = 'Параметры пользователя'
   
 
# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )
 
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user',)


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#admin.site.register(Profile,ProfileAdmin)