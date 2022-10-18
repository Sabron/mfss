# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.acs.views import views_acs

urlpatterns = [
    url(r'^$', views_acs.MainIndex, name='MainIndex'),
    url(r'^sensor/$', views_acs.SensorList, name='SensorList'),
    url(r'sensor_ajax/$', views_acs.sensor_ajax, name='sensor_ajax'),
    url(r'ajax/$', views_acs.get_ajax, name='get_ajax'),
    
    
    ]
