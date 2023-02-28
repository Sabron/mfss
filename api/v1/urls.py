# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.ping, name='ping'),
    url(r'^json/$', views.command, name='Command'),

]
 