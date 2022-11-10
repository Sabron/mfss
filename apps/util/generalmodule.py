# -*- coding: utf-8 -*-
import os
import json
import re
import traceback
from datetime import datetime,timedelta


from django.core.files import File
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.urls import re_path
from django.db.models import Avg, Max, Min
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.db import connection

from sabron.util import logging



def get_context_template():
    context={
              }
    return context




def static(prefix, view=serve, **kwargs):
    """
    Return a URL pattern for serving files in debug mode.

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """
    
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    elif not settings.DEBUG or '://' in prefix:
        # No-op if not in debug mode or a non-local prefix.
        return []
    User.is_authenticated
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]


def getObjectOR404(klassModel, *args, **kwargs):
    objectModel=get_object_or_404(klassModel, pk=kwargs['pk'])
    return objectModel



@login_required(login_url='/accounts/login/')
def get_media_URL(View):
    return settings.MEDIA_URL


@login_required(login_url='/accounts/login/')
def get_media_ROOT(request):
    return settings.MEDIA_ROOT

def convert_number(number):
    return number.replace('A','А').replace('B','В').replace('C','С').replace('E','Е').replace('H','Н').replace('K','К').replace('M','М').replace('O','О').replace('P','Р').replace('T','Т').replace('X','Х').replace('Y','У')



def getJobTime(seccond):
    a = seccond
    h = a//3600
    m = (a//60)%60
    s = a%60
    if m<10:
        m = str('0' + str(m))
    else:
        m = str(m)
    if s<10:
        s = str('0' + str(s))
    else:
        s = str(s)
    return str(h) + ':' + str(m) + ':' + str(s)


def ReturnJson(code,data):
    httpRespon=HttpResponse();
    httpRespon['Content-Type']='application/json'
    httpRespon['Cache-Control']='no-cache,no-store'
    httpRespon['charset']='ASCII'
    httpRespon.status_code=code;
    httpRespon.write(json.dumps(data, sort_keys=True, indent=4))
    return httpRespon;

def Return404():
    httpRespon=HttpResponse();
    httpRespon['Content-Type']='text/plain'
    #httpRespon['charset']='ASCII'
    httpRespon.status_code=404;
    #httpRespon.write(json.dumps(data, sort_keys=True, indent=4))
    return httpRespon;

def ReturnText(text):
    httpRespon=HttpResponse();
    httpRespon['Content-Type']='text/plain'
    httpRespon.write(text)
    return httpRespon;

def ReturnApi(code,data):
    httpRespon=HttpResponse();
    httpRespon['Content-Type']='application/json'
    httpRespon.status_code=code;
    httpRespon.write(json.dumps(data, sort_keys=True, indent=4))
    return httpRespon;

def getSeconds(data1,data2):
    result=0
    diff = data2 - data1
    result=(diff.days*24*60*60)+diff.seconds
    return result


def buildblock(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))