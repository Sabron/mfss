# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.scada.views import views_scada

urlpatterns = [
    url(r'^$', views_scada.MainIndex, name='MainIndex'),
    #url(r'^sensor/$', views_fps.SensorList, name='SensorList'),
    #url(r'sensor_ajax/$', views_fps.sensor_ajax, name='sensor_ajax'),
    #url(r'ajax/$', views_fps.get_ajax, name='get_ajax'),
    
    
    ]

