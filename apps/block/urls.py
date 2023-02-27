# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.block.views import views_block

urlpatterns = [
    url(r'^$', views_block.MainIndex, name='MainIndex'),
    url(r'^sensor/$', views_block.SensorList, name='SensorList'),
    url(r'sensor_ajax/$', views_block.sensor_ajax, name='sensor_ajax'),
    url(r'ajax/$', views_block.get_ajax, name='get_ajax'),
    
    
    ]
