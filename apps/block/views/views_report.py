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

from apps.block.models.model_indicators import BlockIndicators
from apps.block.models.model_sensor import BlockSensor



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

@login_required(login_url='/accounts/login/?next=')
@never_cache
def show_report_ToHTML(request):
    try:
        dict_param=request.POST.dict()
        data_start=datetime.strptime(dict_param['DataStart']+' 00:00:00', "%d.%m.%Y %H:%M:%S")
        data_stop=datetime.strptime(dict_param['DataStop']+' 23:59:59', "%d.%m.%Y %H:%M:%S")
        block_sensor = BlockSensor.objects.filter(id = dict_param['id_block']).first()
        block_indicators_list = BlockIndicators.objects.filter(sensor = block_sensor).filter(date_time__range=[data_start,data_stop]).order_by('date_time').all()
        html="""
            <table id = 'id_table' class='table table-bordered'>
                  <thead>
                    <tr>
                      <th style='width: 15px'>№</th>
                      <th>Датчик</th>
                      <th>Дата</th>
                      <th style='width: 40px'>Статус</th>
                    </tr>
                  </thead>
                  <tbody>
        """
        nom = 0
        for block_indicators in block_indicators_list:
            nom = nom +1
            html = html+"""
                 <tr>
                 <td>"""+str(nom)+"""</td>
                 <td>"""+str(block_indicators.sensor)+"""</td>
                 <td>"""+str(block_indicators.date_time)+"""</td>
                 """
            if block_indicators.value == 0: 
                html = html+"""<td><span class='badge bg-danger'>"""+str(block_indicators.value)+"""</span></td></tr>"""
            else:
                html = html+"""<td><span class='badge bg-success'>"""+str(block_indicators.value)+"""</span></td></tr>"""

                               
                      
                      
                      
                     


        html = html+"""
                  </tbody>
                </table>
        """
        return HttpResponse(html, content_type='application/text')
    except Exception as err:
        logging.error(traceback.format_exc())





def get_ajax(request):
    try:
        if request.method == "POST":
            param=request.GET.dict()
            type = 0
            myquery =Q(active=True)
            if 'type' in param:
                type = param['type']
                myquery &= Q(type=type)
            sensor_list = AcsSensor.objects.filter(myquery).all().order_by('name')
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
        position_list = BlockSensor.objects.values('position').order_by('position').distinct()
        i = 0
        m_zone = []
        for position in position_list:
            i =i+1
            position_dict = dict()
            position_dict.update(id = i)
            position_dict.update(name = position['position'])
            m_zone.append(position_dict)
        param=request.GET.dict()
        type = 0
        sensor_list = BlockSensor.objects.all().order_by('value').order_by('name')
        m_sensor = []
        for sensor in sensor_list:
            str_value=str(sensor.value)
            sensor_dict = dict()
            sensor_dict.update(zone=sensor.zone)
            sensor_dict.update(position=sensor.position)
            sensor_dict.update(sensor=sensor)
            sensor_dict.update(name=sensor.name)
            sensor_dict.update(value=sensor.value)
            sensor_dict.update(connect_time=sensor.connect_time)
            sensor_dict.update(str_value=str_value)
            m_sensor.append(sensor_dict)
        context = {
              'updatepage':True,
              'sensor_list':sensor_list,
              'm_sensor':m_sensor,
              'm_zone':m_zone,
              'type':int(type),
                }
        return render(request, 'block_main.html',context) 


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
def report(request):
    try:
        #if request.user.profile.role == 2: # Администратор системы
        #    return redirect('/management/')
        if request.method == "GET":
            block_list = BlockSensor.objects.all()
            context = {
                'block_list':block_list
                    }
            return render(request, 'block_report.html',context) 
        if request.method == "POST":
            dict_param=request.POST.dict()
            if dict_param['metod']=='create':
                return show_report_ToHTML(request)
            #elif dictParametr['metod']=='download':
            #    return ReportTableWorksToXLS(request)
            
    except Exception as err:
        logging.error(traceback.format_exc())
 

