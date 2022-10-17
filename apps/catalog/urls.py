# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.catalog.views import views_positions
from apps.catalog.views import views_department
from apps.catalog.views import views_country
from apps.catalog.views import views_zone
from apps.catalog.views import views_counterparties
from apps.catalog.views import views_zoneworkers
from apps.catalog.views import views_workers
from apps.catalog.views import views_workersdoc
from apps.catalog.views import views_device
from apps.catalog.views import views_location
from apps.catalog.views import views_checkin
from apps.catalog.views import views_settingsclient

from apps.catalog.views import views_catalog

from apps.util import generalmodule


from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения


urlpatterns = [
   url(r'^$', views_catalog.main_catalog, name='main_catalog'),
   url(r'^device/$', views_device.DeviceList, name='DevicesList'),
   url(r'^devicecmd/$', views_device.DeviceCmd, name='DeviceCmd'),
    
    
   url(r'^department/json/$', views_department.department_json, name='department_json'),
   #url(r'^client/json/$', views_client.client_json, name='client_json'),

   #url(r'^positions/json/$', views_positions.positions_json, name='positions_json'),





 #   url(r'^$', views_checkin.CheckpointsList, name='CheckpointsList'),
#
#    url(r'^positions/$', views_positions.PositionsList, name='PositionsList'),
#    url(r'^positions/add/$', views_positions.PositionsAdd, name='PositionsAdd'),
#    url(r'^positions/json/$', views_positions.PositionsJson, name='PositionsJson'),
#
#
#    url(r'^locations/$', views_location.LocationList, name='LocationList'),
#    url(r'^locations/add/$', views_location.LocationAdd, name='LocationAdd'),
#
#    url(r'^department/$', views_department.DepartmentList, name='DepartmentList'),
#    url(r'^department/add/$', views_department.DepartmentAdd, name='DepartmentAdd'),
#    url(r'^department/json/$', views_department.DepartmentJson, name='DepartmentJson'),
#
#    url(r'^zone/$', views_zone.ZoneList, name='ZoneList'),
#    url(r'^zone/add/$', views_zone.ZoneAdd, name='ZoneAdd'),


#    url(r'^counterparties/$', views_counterparties.CounterpartiesList, name='CounterpartiesList'),
#    url(r'^counterparties/add/$', views_counterparties.CounterpartiesAdd, name='CounterpartiesAdd'),

#   url(r'^workers/$', views_workers.WorkersList, name='WorkersList'),
#    url(r'^workers/add/$', views_workers.WorkersAdd, name='WorkersAdd'),
#   url(r'^workers/zoneworkers/$', views_workers.ZoneWorkersList, name='ZoneWorkersList'),
#    url(r'^workers/adddoc/$', views_workersdoc.AddWorkersDoc, name='AddWorkersDoc'),
#    url(r'^workers/savedoc/$', views_workersdoc.SaveWorkersDoc, name='SaveWorkersDoc'),
#    url(r'^workers/editdoc/$', views_workersdoc.EditWorkersDoc, name='EditWorkersDoc'),
#    url(r'^workers/deletedoc/$', views_workersdoc.DeleteWorkersDoc, name='DeleteWorkersDoc'),

#    url(r'^device/$', views_device.DeviceList, name='DevicesList'),
#    url(r'^devicecmd/$', views_device.DeviceCmd, name='DeviceCmd'),


]

