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

from apps.ktp.models.model_indicators import KtpIndicators
from apps.ktp.models.model_sensor import KtpSensor



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
            sensor_dict = dict()
            sensor_282_t1 = KtpSensor.objects.filter(tag = 'KTP_282.Schetchik_282.SubDevice1.Показания Активная + Реактивная ЭЭ Т1').first()
            indicator_list_282_t1 = KtpIndicators.objects.filter(sensor = sensor_282_t1).order_by('-date_time')[:1]
            value_akt282_t1 = 0
            value_reakt282_t1 = 0
            value_akt282date = ''
            for indicator in indicator_list_282_t1:
                value_akt282_t1 = int(indicator.value_akt)
                value_reakt282_t1 = int(indicator.value_reakt)
                value_akt282date = indicator.date_time

            sensor_282_t2 = KtpSensor.objects.filter(tag = 'KTP_282.Schetchik_282.SubDevice1.Показания Активная + Реактивная ЭЭ Т2').first()
            indicator_list_282_t2 = KtpIndicators.objects.filter(sensor = sensor_282_t2).order_by('-date_time')[:1]
            value_akt282_t2 = 0
            value_reakt282_t2 = 0
            value_akt282date = ''
            for indicator in indicator_list_282_t2:
                value_akt282_t2 = int(indicator.value_akt)
                value_reakt282_t2 = int(indicator.value_reakt)
                value_akt282date = indicator.date_time

            summ282_akt = value_akt282_t1+value_akt282_t2
            summ282_reakt = value_reakt282_t1+value_reakt282_t2
            sensor_dict.update(status=0)
            sensor_dict.update(sensor=282)
            sensor_dict.update(value_akt282_t1=value_akt282_t1)
            sensor_dict.update(value_reakt282_t1=value_reakt282_t1)
            sensor_dict.update(value_akt282_t2=value_akt282_t2)
            sensor_dict.update(value_reakt282_t2=value_reakt282_t2)
            sensor_dict.update(value_akt282date=str(value_akt282date))
            sensor_dict.update(summ282_akt=summ282_akt)
            sensor_dict.update(summ282_reakt=summ282_reakt)
            return generalmodule.ReturnJson(200,sensor_dict)
    except Exception as err:
        logging.error(traceback.format_exc())
        data = dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def MainIndexDefault(request):
     if request.method == "GET":
        sensor_282_t1 = KtpSensor.objects.filter(tag = 'KTP_282.Schetchik_282.SubDevice1.Показания Активная + Реактивная ЭЭ Т1').first()
        indicator_list_282_t1 = KtpIndicators.objects.filter(sensor = sensor_282_t1).order_by('-date_time')[:1]
        value_akt282_t1 = 0
        value_reakt282_t1 = 0
        value_akt282date = ''
        for indicator in indicator_list_282_t1:
            value_akt282_t1 = int(indicator.value_akt)
            value_reakt282_t1 = int(indicator.value_reakt)
            value_akt282date = indicator.date_time

        sensor_282_t2 = KtpSensor.objects.filter(tag = 'KTP_282.Schetchik_282.SubDevice1.Показания Активная + Реактивная ЭЭ Т2').first()
        indicator_list_282_t2 = KtpIndicators.objects.filter(sensor = sensor_282_t2).order_by('-date_time')[:1]
        value_akt282_t2 = 0
        value_reakt282_t2 = 0
        value_akt282date = ''
        for indicator in indicator_list_282_t2:
            value_akt282_t2 = (indicator.value_akt)
            value_reakt282_t2 = (indicator.value_reakt)
            value_akt282date = indicator.date_time

        summ_akt = value_akt282_t1+value_akt282_t2
        summ_reakt = value_reakt282_t1+value_reakt282_t2
        context = {
              'updatepage':True,
              'value_akt282_t1':value_akt282_t1,
              'value_reakt282_t1':value_reakt282_t1,
              'value_akt282_t2':value_akt282_t2,
              'value_reakt282_t2':value_reakt282_t2,
              'value_akt282date':value_akt282date,
              'summ_akt':summ_akt,
              'summ_reakt':summ_reakt
                }
        return render(request, 'ktp_main.html',context) 


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
        if request.method == "POST":
            sensor_dict = dict()
            param = request.POST.dict()
            sensor = AcsSensor.objects.filter(id=param['id']).first()
            critical_type = sensor.critical_type
            connect_time = sensor.connect_time
            value = sensor.value
            end_date=sensor.connect_time
            if param['sensor_type'] == 'sec':
                strftime = "%H:%M:%S"
                start_date = end_date - timedelta(seconds=30)
            elif param['sensor_type'] == 'min':
                strftime = "%H:%M"
                start_date = end_date - timedelta(minutes=30)
            else:
                strftime = "%H:00"
                start_date = end_date - timedelta(hours=30)
            
            sensor_links = AcsIndicators.objects.filter(sensor=sensor).filter(date_time__range=[start_date,end_date]).order_by('date_time').order_by('id')
            strftimeend = "%d.%m.%Y %H"
            m_sensor = []
            value_old = 0
            for i in range(31):
                if param['sensor_type'] == 'sec':
                    strftimeend = "%d.%m.%Y %H:%M:%S"
                    date_time = start_date + timedelta(seconds=i)
                    start_date_day = date_time
                    end_date_day = date_time+ timedelta(milliseconds=1000)
                elif param['sensor_type'] == 'min':
                    strftimeend = "%d.%m.%Y %H:%M"
                    date_time = start_date + timedelta(minutes=i)
                    start_date_day = datetime(date_time.year, date_time.month, date_time.day,date_time.hour,date_time.minute,0)
                    end_date_day = datetime(date_time.year, date_time.month, date_time.day,date_time.hour,date_time.minute,59,9999)
                else:
                    strftimeend = "%d.%m.%Y %H"
                    date_time = start_date + timedelta(hours=i)
                    start_date_day = datetime(date_time.year, date_time.month, date_time.day,date_time.hour,0,0)
                    end_date_day = datetime(date_time.year, date_time.month, date_time.day,date_time.hour,59,59,9999)
                sensor_dict = dict()
                sensor_dict.update(date_max=str(connect_time))
                if critical_type =="max":
                    value_date =0
                else:
                    value_date =9999999
                result = sensor_links.filter(date_time__range=[start_date_day,end_date_day]).aggregate(Max('value'))
                sensor_dict.update(date_time = date_time.strftime(strftime))
                if result['value__max'] == None:
                    sensor_dict.update(value = value_old)
                else:
                    value_old = result['value__max']/sensor.ratio
                    sensor_dict.update(value = result['value__max']/sensor.ratio)
                m_sensor.append(sensor_dict)
            return generalmodule.ReturnJson(200,m_sensor)

    except Exception as err:
        logging.error(traceback.format_exc())


@login_required(login_url='/accounts/login/?next=')
@never_cache
def sensor_ajax_1(request):
    try:
        if request.method == "POST":
            sensor_dict = dict()
            param = request.POST.dict()
            sensor = AcsSensor.objects.filter(id=param['id']).first()
            strftime = "%H:%M:%S"
            if param['sensor_type'] == 'sec':
                strftime = "%H:%M:%S"
                sensor_list = AcsIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:100]
                #sensor_list = AcsIndicators.objects.filter(sensor=sensor).annotate(
                #        date_value=TruncSecond('date_time')).values('date_time', 'date_value', 'value', 'sensor__ratio').order_by('-date_value').distinct('date_value')[:30]
            elif param['sensor_type'] == 'min':
                strftime = "%H:%M"
                sensor_list = AcsIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:3600]
                #sensor_list = AcsIndicators.objects.filter(sensor=sensor).annotate(
                #        date_value=TruncMinute('date_time')).values('date_time','date_value', 'value', 'sensor__ratio').order_by('-date_value').distinct('date_value')[:30]
            else:
                strftime = "%H:00"
                sensor_list = AcsIndicators.objects.filter(sensor=sensor).order_by('-date_time')[:120000]
                #sensor_list = AcsIndicators.objects.filter(sensor=sensor).annotate(
                #        date_value=TruncHour('date_time')).values('date_value', 'date_value','value', 'sensor__ratio').order_by('-date_value').distinct('date_value')[:30]
                #sensor_list = AcsIndicators.objects.filter(sensor=sensor).order_by('-date_time')
                #m_sensor = []
                #data_list =list()
                #count = 0
                #for sensor in sensor_list:
                    #logging.message(sensor)
                #    data = sensor.date_time.strftime(strftime)
                #    if data in data_list:
                #        continue;
                #    data_list.append(data)
                #    sensor_dict = dict()
                #    sensor_dict.update(date_time=sensor.date_time.strftime(strftime))
                    #sensor_dict.update(date_time=sensor['date_value'].strftime("%d-%m %H:%M:%S"))
                #    sensor_dict.update(value=sensor.value / sensor.sensor.ratio)
                #    m_sensor.append(sensor_dict)
                #    count = count+1
                #    if count > 30:
                #        return generalmodule.ReturnJson(200,m_sensor) 
                #return generalmodule.ReturnJson(200,m_sensor)
            
            m_sensor = []
            data_list =list()
            count = 0
            date_max =0
            for sensor in sensor_list:
                if date_max == 0:
                    date_max = sensor.date_time
                else: 
                    if date_max < sensor.date_time:
                        date_max = sensor.date_time
                data = sensor.date_time.strftime(strftime)
                if data in data_list:
                    continue;
                data_list.append(data)
                sensor_dict = dict()
                sensor_dict.update(date_time=sensor.date_time.strftime(strftime))
                sensor_dict.update(value=sensor.value / sensor.sensor.ratio)
                sensor_dict.update(date_max=str(date_max))
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
        print('main')
        return MainIndexDefault(request)
    except Exception as err:
        logging.error(traceback.format_exc())
 

