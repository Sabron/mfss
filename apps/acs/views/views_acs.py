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
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond,Greatest,
)

from apps.acs.models.model_indicators import AcsIndicators
from apps.acs.models.model_sensor import AcsSensor


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
            sensor_list = AcsSensor.objects.filter(active=True).all().order_by('name')
            m_sensor = []
            for sensor in sensor_list:
                sensor_dict = dict()
                sensor_dict.update(sensor_id=sensor.id)
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
                if sensor.critical_type == 'max':
                    if sensor.value / sensor.ratio >= sensor.critical_value:
                        color = 'bg-danger'
                else:
                    if sensor.value / sensor.ratio <= sensor.critical_value:
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
        sensor_list = AcsSensor.objects.filter(active=True).all().order_by('name')
        m_sensor = []
        for sensor in sensor_list:
            str_value=str(sensor.value / sensor.ratio).replace(',','.')
            sensor_dict = dict()
            sensor_dict.update(sensor=sensor)
            sensor_dict.update(value=sensor.value / sensor.ratio)
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
            if sensor.critical_type == 'max':
                if sensor.value / sensor.ratio >= sensor.critical_value:
                    color = 'bg-danger'
            else:
                if sensor.value / sensor.ratio <= sensor.critical_value:
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
            start_date = now - timedelta(hours=0, minutes=0)
            sensor_list = AcsIndicators.objects.filter(sensor=sensor).filter(date_time__range=[start_date, datetime.now()]).all().order_by('-date_time')
            sensor_str = ''
            for sensor_in in sensor_list:
                sensor_str = sensor_str+str(sensor_in.value).replace(',','.')+','
            context = {
                    'sensor':sensor,
                    'sensor_list':sensor_list,
                    'sensor_str':sensor_str,
                    }
            return render(request, 'acs_sensor_list.html',context) 
    except Exception as err:
        logging.error(traceback.format_exc())

@login_required(login_url='/accounts/login/?next=')
@never_cache
def sensor_ajax(request):
    try:
        if request.method == "GET":
            sensor_dict = dict()
            param = request.GET.dict()
            sensor = AcsSensor.objects.filter(id=param['id']).first()
            strftime = "%H:%M:%S"
            if param['sensor_type'] == 'sec':
                sensor_list = AcsIndicators.objects.filter(sensor=sensor).annotate(
                        date_value=TruncSecond('date_time')).values('date_time', 'date_value', 'value', 'sensor__ratio').order_by('-date_value').distinct('date_value')[:30]
            elif param['sensor_type'] == 'min':
                strftime = "%H:%M"
                sensor_list = AcsIndicators.objects.filter(sensor=sensor).annotate(
                        date_value=TruncMinute('date_time')).annotate(zn_value =Max('value')).values('date_time','date_value', 'value', 'sensor__ratio').order_by('-date_value').distinct()[:30]
            else:
                strftime = "%H:%M"
                sensor_list = AcsIndicators.objects.filter(sensor=sensor).annotate(
                        date_value=TruncHour('date_time')).annotate(zn_value =Max('value')).values('date_value','zn_value', 'value', 'sensor__ratio').order_by('-date_value').distinct()[:30]
            m_sensor = []
            for sensor in sensor_list:
                #logging.message(sensor)
                sensor_dict = dict()
                sensor_dict.update(date_time=sensor['date_value'].strftime(strftime))
                #sensor_dict.update(date_time=sensor['date_value'].strftime("%d-%m %H:%M:%S"))
                sensor_dict.update(value=sensor['value'] / sensor['sensor__ratio'])
                m_sensor.append(sensor_dict)
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
 

