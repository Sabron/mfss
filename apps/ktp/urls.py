# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.ktp.views import views_ktp
#from apps.ktp.views import views_report

urlpatterns = [
    url(r'^$', views_ktp.MainIndex, name='MainIndex'),
    #url(r'^sensor/$', views_acs.SensorList, name='SensorList'),
    #url(r'sensor_ajax/$', views_acs.sensor_ajax, name='sensor_ajax'),
    url(r'ajax/$', views_ktp.get_ajax, name='get_ajax'),
    #url(r'^report/$', views_report.report_list, name='report_list'),
    
    
    ]
