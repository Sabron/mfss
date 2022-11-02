# -*- coding: utf-8 -*-
import traceback
import requests
import random

from datetime import datetime,timedelta
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Avg, Max, Min

from apps.eps.models.model_tags import Tag
from apps.eps.models.model_tagdates import TagDate

from apps.util import generalmodule
from sabron.util import logging


def get_ajax(request):
    try:
        if request.method == "POST":
            Tag_list = Tag.objects.all().order_by('name')
            m_sensor = []
            for tag in Tag_list:
                #x = (int(tag.x)+random.randint(1,5))*(1014 / 42)
                #y =829 - (int(tag.y)+random.randint(1,5))*(1014/42)
                x = int(int(tag.x)*22)
                y =792 - int(int(tag.y)*22)
                tag_dict = dict()
                tag_dict.update(id=tag.id)
                tag_dict.update(name=tag.name)
                tag_dict.update(sn=tag.sn)
                tag_dict.update(le_status=tag.le_status)
                #tag_dict.update(x=int(tag.x))
                #tag_dict.update(y=int(tag.y))
                tag_dict.update(x=x)
                tag_dict.update(y=y)
                tag_dict.update(z=int(tag.z))
                m_sensor.append(tag_dict)
            
            return generalmodule.ReturnJson(200,m_sensor)
    except Exception as err:
        logging.error(traceback.format_exc())
        data = dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def get_tag(request):
    try:
        if request.method == "POST":
            Tag_list = Tag.objects.all().order_by('name')
            m_sensor = []
            for tag in Tag_list:
                tag_dict = dict()
                tag_dict.update(id=tag.id)
                tag_dict.update(name=tag.name)
                tag_dict.update(sn=tag.sn)
                tag_dict.update(le_status=tag.le_status)
                tag_dict.update(x=int(tag.x))
                tag_dict.update(y=int(tag.y))
                tag_dict.update(z=int(tag.z))
                m_sensor.append(tag_dict)
            return generalmodule.ReturnJson(200,m_sensor)
    except Exception as err:
        logging.error(traceback.format_exc())
        data = dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def main_index_default(request):
     if request.method == "GET":
        context = {
                   }
        return render(request, 'eps_main.html',context) 


def map(request):
     if request.method == "GET":
        tag_list = Tag.objects.all().order_by('name')
        context = {
                    'tag_list':tag_list,
                   }
        return render(request, 'eps_map.html',context) 

@login_required(login_url='/accounts/login/?next=')
@never_cache
def main_index(request):
    try:
        return main_index_default(request)
    except Exception as err:
        logging.error(traceback.format_exc())
 

