# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.dcs.views import views_dcs
from apps.dcs.views import views_report

urlpatterns = [
    url(r'^$', views_dcs.MainIndex, name='MainIndex'),
    url(r'^sensor/$', views_dcs.SensorList, name='SensorList'),
    url(r'sensor_ajax/$', views_dcs.sensor_ajax, name='sensor_ajax'),
    url(r'ajax/$', views_dcs.get_ajax, name='get_ajax'),
    url(r'^report/$', views_report.report_list, name='report_list'),
    
    ]
