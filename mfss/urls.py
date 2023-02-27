# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include # Используйте include() чтобы добавлять URL из каталога приложения
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico'), name='favicon'),
    url(r'^$', RedirectView.as_view(url='/main/', permanent=True)), #Перенаправляет все запросы 
    url(r'^admin/', admin.site.urls),
    url(r'^main/', include('apps.main.urls')),
    url(r'^acs/', include('apps.acs.urls')),
    url(r'^fps/', include('apps.fps.urls')),
    url(r'^dcs/', include('apps.dcs.urls')),
    url(r'^eps/', include('apps.eps.urls')),
    url(r'^scada/', include('apps.scada.urls')),
    url(r'^block/', include('apps.block.urls')),
    url(r'^management/', include('apps.management.urls')),

    url(r'^accounts/logout/', views.user_logout, name='user_logout'),
    url(r'^accounts/', views.user_login, name='user_login'),

    url('bot/', include('tgbot.urls')),
]

urlpatterns += static(settings.DOWNLOAD_URL, document_root=settings.DOWNLOAD_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

