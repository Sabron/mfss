# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.model_country import Country
from .models.model_partners import Partner
from .models.model_violations import Violation
from .models.model_clients import Clients
from .models.model_counterparties import Counterparties
from .models.model_positions import Positions
from .models.model_zone import Zone
from .models.model_department import Department
from .models.model_device import Device
from .models.model_workers import Workers
from .models.model_deviceparametrs import DeviceParametrs
from .models.model_location import Location
from .models.model_checkpoints import Checkpoints
from .models.model_fingerprints import Fingerprints
from .models.model_faceprints import Faceprints
from .models.model_buffercmd import Buffercmd
from .models.model_zoneworkers import ZoneWorkers
from .models.model_settingsclient import Settingsclient
from .models.model_violationlog import Violationlog
from .models.model_workersinjob import Workersinjob
from .models.model_workersdoc import Workersdoc
from .models.model_biodata import Biodata
from .models.model_workersbiophoto import WorkersBioPhoto
from .models.model_timesheet import TimeSheet
from .models.model_partners import Partner

from apps.catalog.models.model_usersettings import UserSettings


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin): #Настройки пользователя
    list_display = ('name','idcode')

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin): #Настройки пользователя
    list_display = ('user',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin): #объекты
    list_display = ('name','client','TimeZone','latitude','longitude','autoexit')
    list_filter = ('client',)


@admin.register(ZoneWorkers)
class ZoneWorkersAdmin(admin.ModelAdmin): #Зоны доступа
    list_display = ('client','workers','name','zone')
    list_filter = ('client',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin): #Зоны
    ordering = ('name',)
    list_display = ('client','location','name')
    list_filter = ('client','location',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin): #Устройства
    list_display = ('name','SN','connect_time','client','Zone','TypeJob','UserCount','partner')
    #list_display = ('name','SN','client','Zone','TypeJob','UserCount','partner',)
    list_filter = ('client','partner')

@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')
    fields = ['name', 'client' ]
    list_filter = ('client',)



class ZoneWorkersInline(admin.TabularInline):
    model = ZoneWorkers
    list_filter = ('client',)

@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ('name','client','id','tabnomer', 'sex_workers','department','datebirth','position','phone')
    list_filter = ('client',)
    search_fields = ('name',)

@admin.register(Checkpoints)
class CheckpointsAdmin(admin.ModelAdmin): #Отметки
    list_display = ('workers','checkin','location','verifycode','checktype','device','valid')
    list_filter = ('client','zone')
    search_fields = ('workers__name',)

@admin.register(DeviceParametrs)
class DeviceParametrsAdmin(admin.ModelAdmin): #Параметры устройства
    list_display = ('name','value','device')
    list_filter = ('device',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin): #Подразделения
    list_display = ('name','client')
    list_filter = ('client',)
    
@admin.register(Buffercmd)
class BuffercmdAdmin(admin.ModelAdmin): #Буфер команд
    list_display = ('device','commandcode','key','datecmd')
    list_filter = ('device',)

@admin.register(Faceprints)
class FaceprintsAdmin(admin.ModelAdmin):
     list_display = ('workers','client')
     list_filter = ('client',)

@admin.register(Fingerprints)
class FingerprintsAdmin(admin.ModelAdmin):
     list_display = ('workers','client')
     list_filter = ('client',)
   
@admin.register(Workersinjob)
class WorkersinjobAdmin(admin.ModelAdmin):
     list_display = ('workers','client','location','checkin','checktype')
     list_filter = ('client',)

@admin.register(Biodata)
class BiodataAdmin(admin.ModelAdmin):
     list_display = ('workers','type','majorver','minorver')
     list_filter = ('client','workers')

@admin.register(WorkersBioPhoto)
class WorkersBioPhotoAdmin(admin.ModelAdmin):
     list_display = ('workers','type')
     list_filter = ('client',)

class SettingsclientInline(admin.TabularInline):
    
    model = Settingsclient
    can_delete = False
    verbose_name_plural = 'Параметры клиента'

@admin.register(Settingsclient)
class SettingsclientAdmin(admin.ModelAdmin):
    list_display = ('client', 'type','keyname','name','value')
    fields = ['client','type','keyname','name','value']

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name','adress','inn','partner')
    list_filter = ('partner',)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)


     

admin.site.register(Violation)
admin.site.register(Violationlog)





