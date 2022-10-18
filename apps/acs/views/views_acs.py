# -*- coding: utf-8 -*-
import traceback
import requests

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


from apps.acs.models.model_indicators import AcsIndicators
from apps.acs.models.model_sensor import AcsSensor


from apps.util import generalmodule
from sabron.util import logging


def get_ajax(request):
    try:
        if request.method == "POST":
            sensor_list = AcsSensor.objects.filter(active=True).all().order_by('name')
            m_sensor = []
            for sensor in sensor_list:
                sensor_dict = dict()
                sensor_dict.update(sensor_id=sensor.id)
                sensor_dict.update(value=sensor.value/100)
                sensor_dict.update(critical_value=sensor.critical_value)
                sensor_dict.update(unit=sensor.unit)
                pecent = ((sensor.value/100)* 100) / sensor.critical_value
                sensor_dict.update(pecent_value=pecent)
                #sensor.critical_value
                #color=0 зеленый
                #color=1 желтый
                #color=2 красный
                color = 'bg-success'
                if sensor.critical_type == 'max':
                    if sensor.value/100 >= sensor.critical_value:
                        color = 'bg-danger'
                else:
                    if sensor.value/100 <= sensor.critical_value:
                        color = 'bg-danger'
                sensor_dict.update(color=color)
                m_sensor.append(sensor_dict)
                data = dict()
            return generalmodule.ReturnJson(200,m_sensor)
    except Exception as err:
        logging.error(traceback.format_exc())
        data = dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def MainIndexDefault(request):
     if request.method == "GET":
        sensor_list = AcsSensor.objects.filter(active=True).all().order_by('name')
        m_sensor = []
        for sensor in sensor_list:
            print(sensor.critical_type)
            sensor_dict = dict()
            sensor_dict.update(sensor=sensor)
            sensor_dict.update(value=sensor.value/100)
            sensor_dict.update(critical_value=sensor.critical_value)
            sensor_dict.update(unit=sensor.unit)
            #sensor.critical_value
            #color=0 зеленый
            #color=1 желтый
            #color=2 красный
            color = 'bg-success'
            if sensor.critical_type == 'max':
                if sensor.value/100 >= sensor.critical_value:
                    color = 'bg-danger'
            else:
                if sensor.value/100 <= sensor.critical_value:
                    color = 'bg-danger'
            sensor_dict.update(color=color)
            m_sensor.append(sensor_dict)
        context = {
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
            param = request.GET.dict()
            sensor = AcsSensor.objects.filter(id=param['id']).first()
            now = datetime.now()
            start_date = now - timedelta(hours=0, minutes=0,seconds=5)
            logging.message(start_date)
            logging.message(datetime.now())
            
            sensor_list = AcsIndicators.objects.filter(sensor=sensor).filter(date_time__range=[start_date, datetime.now()]).all().order_by('date_time')
            logging.message(str(sensor_list))
            context = {
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
        #if request.user.profile.role == 2: # Администратор системы
        #    return redirect('/management/')

        return MainIndexDefault(request)
    except Exception as err:
        logging.error(traceback.format_exc())
 

