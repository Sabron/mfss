# -*- coding: utf-8 -*-
import traceback
import requests
import math

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
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond,Greatest,
)

from apps.fps.models.model_indicators import FpsIndicators
from apps.fps.models.model_sensor import FpsSensor


from apps.util import generalmodule
from sabron.util import logging

def float_range(A, L=None, D=None):
    #Use float number in range() function
    # if L and D argument is null set A=0.0 and D = 1.0
    if L == None:
        L = A + 0.0
        A = 0.0
    if D == None:
        D = 1.0
    while True:
        if D > 0 and A >= L:
            break
        elif D < 0 and A <= L:
            break
        yield ("%g" % A) # return float number
        A = A + D
#end of function float_range()

def get_ajax(request):
    try:
        if request.method == "POST":
            param=request.GET.dict()
            type = 0
            myquery =Q(active=True)
            if 'type' in param:
                type = param['type']
                myquery &= Q(type=type)
            sensor_list = FpsSensor.objects.filter(myquery).all().order_by('name')
            m_sensor = []
            for sensor in sensor_list:
                print(type)
                sensor_dict = dict()
                sensor_dict.update(type=sensor.type)
                sensor_dict.update(sensor_id=sensor.id)
                sensor_dict.update(max_value=sensor.max_value)
                sensor_dict.update(value=sensor.value / sensor.ratio)
                sensor_dict.update(critical_value=sensor.critical_value)
                sensor_dict.update(unit=sensor.unit)
                pecent = ((sensor.value / sensor.ratio) * 100) / sensor.critical_value
                sensor_dict.update(pecent_value=pecent)
                #sensor.critical_value
                #color=0 зеленый
                #color=1 желтый
                #color=2 красный
                color = 'bg-success'
                if sensor.value / sensor.ratio <= sensor.danger_value_to:
                    color = 'bg-danger'
                sensor_dict.update(color=color)
                m_sensor.append(sensor_dict)
            return generalmodule.ReturnJson(200,m_sensor)
    except Exception as err:
        logging.error(traceback.format_exc())
        data = dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def MainIndexDefault(request):
     if request.method == "GET":
        param=request.GET.dict()
        type = 0
        myquery =Q(active=True)
        if 'type' in param:
            type = param['type']
            myquery &= Q(type=type)
        sensor_list = FpsSensor.objects.filter(myquery).all().order_by('name')
        m_sensor = []
        m_zone = []
        for sensor in sensor_list:
            str_value=str(round(sensor.value / sensor.ratio,2)).replace(',','.')
            sensor_dict = dict()
            sensor_dict.update(zone=sensor.zone)
            sensor_dict.update(type=sensor.type)
            sensor_dict.update(sensor=sensor)
            sensor_dict.update(name=sensor.name)
            sensor_dict.update(value=sensor.value / sensor.ratio)
            sensor_dict.update(max_value=sensor.max_value)
            sensor_dict.update(str_value=str_value)
            sensor_dict.update(critical_value=sensor.critical_value)
            sensor_dict.update(str_critical_value=str(sensor.critical_value).replace(',','.'))
            sensor_dict.update(unit=sensor.unit)
            sensor_dict.update(scale=sensor.scale)
            sensor_dict.update(norm_value_from=str(sensor.norm_value_from).replace(',','.'))
            sensor_dict.update(norm_value_to=str(sensor.norm_value_to).replace(',','.'))
            sensor_dict.update(danger_value_from=str(sensor.danger_value_from).replace(',','.'))
            sensor_dict.update(danger_value_to=str(sensor.danger_value_to).replace(',','.'))
            sensor_dict.update(critical_value_from=str(sensor.critical_value_from).replace(',','.'))
            sensor_dict.update(critical_value_to=str(sensor.critical_value_to).replace(',','.'))
            #sensor.critical_value
            #color=0 зеленый
            #color=1 желтый
            #color=2 красный
            color = 'bg-success'
            #if sensor.critical_type == 'max':
            #    if sensor.value / sensor.ratio >= sensor.critical_value:
            #        color = 'bg-danger'
            #else:
            if sensor.value / sensor.ratio <= sensor.danger_value_to:
                color = 'bg-danger'
            sensor_dict.update(color=color)
            m_sensor.append(sensor_dict)
            if sensor.zone not in m_zone:
                m_zone.append(sensor.zone)
        context = {
              'updatepage':True,
              'sensor_list':sensor_list,
              'm_sensor':m_sensor,
              'm_zone':m_zone,
              'type':int(type),
                }
        return render(request, 'fps_main.html',context) 


@login_required(login_url='/accounts/login/?next=')
@never_cache
def SensorList(request):
    try:
        if request.method == "GET":
            param = request.GET.dict()
            sensor = FpsSensor.objects.filter(id=param['id']).first()
            now = datetime.now()
            start_date = now - timedelta(hours=0, minutes=0)
            sensor_list = FpsIndicators.objects.filter(sensor=sensor).filter(date_time__range=[start_date, datetime.now()]).all().order_by('-date_time')
            sensor_str = ''
            for sensor_in in sensor_list:
                sensor_str = sensor_str+str(sensor_in.value).replace(',','.')+','
            context = {
                    'sensor':sensor,
                    'sensor_list':sensor_list,
                    'sensor_str':sensor_str,
                    }
            return render(request, 'fps_sensor_list.html',context) 
    except Exception as err:
        logging.error(traceback.format_exc())

@login_required(login_url='/accounts/login/?next=')
@never_cache
def sensor_ajax(request):
    try:
        if request.method == "POST":
            sensor_dict = dict()
            param = request.POST.dict()
            sensor = FpsSensor.objects.filter(id=param['id']).first()
            strftime = "%H:%M:%S"
            if param['sensor_type'] == 'sec':
                strftime = "%H:%M:%S"
                sensor_list = FpsIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:100]
            elif param['sensor_type'] == 'min':
                strftime = "%H:%M"
                sensor_list = FpsIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:3600]
            else:
                strftime = "%H:00"
                sensor_list = FpsIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:120000]
            
            m_sensor = []
            data_list =list()
            count = 0
            for sensor in sensor_list:
                #logging.message(sensor)
                data = sensor.date_time.strftime(strftime)
                if data in data_list:
                    continue;
                data_list.append(data)
                sensor_dict = dict()
                sensor_dict.update(date_time=sensor.date_time.strftime(strftime))
                #sensor_dict.update(date_time=sensor['date_value'].strftime("%d-%m %H:%M:%S"))
                sensor_dict.update(value=sensor.value / sensor.sensor.ratio)
                m_sensor.append(sensor_dict)
                count = count+1
                if count > 30:
                    return generalmodule.ReturnJson(200,m_sensor) 
            return generalmodule.ReturnJson(200,m_sensor) 
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
 

