# -*- coding: utf-8 -*-
import traceback
import datetime
import requests

from datetime import datetime
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


from apps.acs.models.model_indicators import AcsIndicators
from apps.acs.models.model_sensor import AcsSensor


from apps.util import generalmodule
from sabron.util import logging


def get_ajax(request):
    try:
        data=dict()
    except Exception as err:
        logging.error(traceback.format_exc())
        data=dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def MainIndexDefault(request):
     if request.method == "GET":
        sensor_list = AcsSensor.objects.filter(active=True).all().order_by()
        m_sensor=[]
        for sensor in sensor_list:
            print(sensor.critical_type)
            sensor_dict=dict()
            sensor_dict.update(sensor=sensor)
            sensor_dict.update(value=sensor.value)
            sensor_dict.update(critical_value=sensor.critical_value)
            #sensor.critical_value
            #color=0 зеленый
            #color=1 желтый
            #color=2 красный
            color='bg-success'
            if sensor.critical_value=='max':
                if sensor.value>=sensor.critical_value:
                    color='bg-danger'
            else:
                if sensor.value<=sensor.critical_value:
                    color='bg-danger'
            sensor_dict.update(color=color)
            m_sensor.append(sensor_dict)
        context={
              'updatepage':True,
              'sensor_list':sensor_list,
              'm_sensor':m_sensor,
                }
        return render(request, 'acs_main.html',context) 


@login_required(login_url='/accounts/login/?next=')
@never_cache
def SensorList(request):
    try:
        if request.method == "GET":
            param=request.GET.dict()
            sensor=AcsSensor.objects.filter(id=param['id']).first()
            sensor_list = AcsIndicators.objects.filter(sensor=sensor).all().order_by('date_time')
            context={
                    'sensor':sensor,
                    'sensor_list':sensor_list,
                    }
            return render(request, 'acs_sensor_list.html',context) 
    except Exception as err:
        logging.error(traceback.format_exc())


@login_required(login_url='/accounts/login/?next=')
@never_cache
def MainIndex(request):
    try:
        if request.user.profile.role == 2: # Администратор системы
            return redirect('/management/')

        return MainIndexDefault(request)
    except Exception as err:
        logging.error(traceback.format_exc())
 

