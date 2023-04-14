# -*- coding: utf-8 -*-
import traceback
import requests
#import locale
#locale.setlocale(
#    category=locale.LC_ALL,
#    locale="ru"  # Note: do not use "de_DE" as it doesn't work
#)


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

from apps.fp.models.model_indicators import FpIndicators
from apps.fp.models.model_sensor import FpSensor


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
            sensor_list = FpSensor.objects.filter(active=True).all().order_by('name')
            m_sensor = []
            for sensor in sensor_list:
                sensor_dict = dict()
                sensor_dict.update(sensor_id=sensor.id)
                sensor_dict.update(code=sensor.value)
                sensor_dict.update(connect_time = sensor.connect_time)
                m_sensor.append(sensor_dict)
            return generalmodule.ReturnJson(200,m_sensor)
    except Exception as err:
        logging.error(traceback.format_exc())
        data = dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def MainIndexDefault(request):
     if request.method == "GET":
        sensor_list = FpSensor.objects.filter(active=True).all().order_by('name')
        m_sensor = []
        m_zone = []
        for sensor in sensor_list:
            connect_time = sensor.connect_time
            print(type(connect_time))
            sensor_dict = dict()
            sensor_dict.update(zone=sensor.zone)
            sensor_dict.update(sensor=sensor)
            sensor_dict.update(name=sensor.name)
            sensor_dict.update(code=sensor.code)
            sensor_dict.update(connect_time = connect_time)
            m_sensor.append(sensor_dict)
        context = {
              'updatepage':True,
              'sensor_list':sensor_list,
              'm_sensor':m_sensor,
                }
        return render(request, 'fp_main.html',context) 


@login_required(login_url='/accounts/login/?next=')
@never_cache
def SensorList(request):
    try:
        if request.method == "GET":
            param = request.GET.dict()
            sensor = FpSensor.objects.filter(id=param['id']).first()
            now = datetime.now()
            start_date = now - timedelta(hours=0, minutes=0)
            sensor_list = FpIndicators.objects.filter(sensor=sensor).filter(date_time__range=[start_date, datetime.now()]).all().order_by('-date_time')
            sensor_str = ''
            for sensor_in in sensor_list:
                sensor_str = sensor_str+str(sensor_in.value).replace(',','.')+','
            context = {
                    'sensor':sensor,
                    'sensor_list':sensor_list,
                    'sensor_str':sensor_str,
                    }
            return render(request, 'fp_sensor_list.html',context) 
    except Exception as err:
        logging.error(traceback.format_exc())

@login_required(login_url='/accounts/login/?next=')
@never_cache
def sensor_ajax(request):
    try:
        if request.method == "POST":
            sensor_dict = dict()
            param = request.POST.dict()
            sensor = FpSensor.objects.filter(id=param['id']).first()
            strftime = "%H:%M:%S"
            if param['sensor_type'] == 'sec':
                strftime = "%H:%M:%S"
                sensor_list = FpIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:100]
            elif param['sensor_type'] == 'min':
                strftime = "%H:%M"
                sensor_list = FpIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:3600]
            else:
                strftime = "%H:00"
                sensor_list = FpIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:120000]
            
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
 



