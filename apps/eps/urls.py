# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.eps.views import views_eps

urlpatterns = [
    url(r'^$', views_eps.main_index, name='main_index'),
    url(r'^map/$', views_eps.map, name='map'),
    #№url(r'sensor_ajax/$', views_acs.sensor_ajax, name='sensor_ajax'),
    url(r'ajax/$', views_eps.get_ajax, name='get_ajax'),
    url(r'gettag/$', views_eps.get_tag, name='get_tag'),
    
    
    ]
