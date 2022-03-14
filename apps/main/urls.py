# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения

from apps.main.views import views_main

urlpatterns = [
    url(r'^$', views_main.MainIndex, name='MainIndex'),
    url(r'ajax/$', views_main.get_ajax, name='get_ajax'),
    
    ]
