# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.fp.views import views_fp

urlpatterns = [
    url(r'^$', views_fp.MainIndex, name='MainIndex'),
    #url(r'^sensor/$', views_fps.SensorList, name='SensorList'),
    #url(r'sensor_ajax/$', views_fps.sensor_ajax, name='sensor_ajax'),
    url(r'ajax/$', views_fp.get_ajax, name='get_ajax'),
    
    
    ]


