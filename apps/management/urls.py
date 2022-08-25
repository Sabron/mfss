# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.management.views import views_management
from django.contrib.auth.decorators import login_required
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения



urlpatterns = [
    url(r'^$', views_management.main_index, name='main_index'),
]
