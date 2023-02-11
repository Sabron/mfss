import os, django
import requests
import requests.exceptions as rex
import sys
import calendar
import uuid
import datetime as DT
import pytz
import json
#import maya
import random
import time
import traceback

from datetime import datetime, timedelta,date
from requests.auth import HTTPBasicAuth
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mfss.settings')
django.setup() 

from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.db.models import Sum

from apps.ops.models.model_mfsb import Mfsb
from apps.ops.models.model_mfsb_skada import MfsbSkada
from apps.ops.models.model_mfsb_ppz import MfsbPpz
from apps.ops.models.model_mfsb_skpv import MfsbSkpv


from apps.main.models.model_datamfsb import DataMfsb
from apps.main.models.model_datamfsb_skada import DataMfsbSkada
from apps.main.models.model_datamfsb_ppz import DataMfsbPpz
from apps.main.models.model_datamfsb_skpv import DataMfsbSkpv


from apps.acs.models.model_sensor import AcsSensor
from apps.acs.models.model_indicators import AcsIndicators

from apps.fps.models.model_sensor import FpsSensor
from apps.fps.models.model_indicators import FpsIndicators


from apps.eps.models.model_tags import Tag
from apps.eps.models.model_tagdates import TagDate
from apps.eps.models.model_anchors import Anchors

from apps.fp.models.model_code_bolid import CodeBolid

from django.contrib.auth.models import User





from django.conf import settings
from django.core.files import File




from datetime import datetime, timedelta, timezone



from sabron.util import logging


def update_acs():
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    for data in data_mfsb:
        print(str(data.date)+' : '+data.name)
        sensor_link = AcsSensor.objects.filter(tag=data.name).filter(active=True).first()
        print(str(sensor_link))
        if sensor_link is not None:
            Acs_Indicators = AcsIndicators.objects.create(
                date_time =data.date,
                sensor = sensor_link,
                value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date 
            sensor_link.save()
            data.check = True
            data.save()
            print(Acs_Indicators)


def test_Mfsb():
    mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all();
    for mfsb in mfsb_list:
        print(mfsb.name+'   :  '+str(mfsb.values)+'   :  '+str(mfsb.date)+'   :  '+str(mfsb.check))
        datd_mfsb = DataMfsb.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
        if datd_mfsb is None:
            DataMfsb.objects.create(
                date=datetime.now(),
                name=mfsb.name,
                values=mfsb.values,
                check=mfsb.check)
        mfsb.check = True
        mfsb.save()
        update_acs()

def update_eps():
    try:
        r=requests.post("https://87.103.198.150:56443/CFG-API/auth",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            print(r.status_code)
            return
        r=requests.get("https://87.103.198.150:56443/CFG-API/monitor/tags",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            print(r.status_code)
            return
        mystr=r.json()
        print(mystr)
        for tag in mystr['items']:
            #timezone_date_time_obj = maya.parse(tag['time']).datetime(to_timezone='Europe/Moscow', naive=False)
            tag_link = Tag.objects.filter(sn=tag['sn']).first()
            if tag_link is None:
                tag_link = Tag.objects.create(
                    name=tag['sn'],
                    sn=tag['sn'],
                    descr=tag['descr'],
                    origin=tag['origin'],
                    le_status =tag['le_status'],
                    x = tag['x'],
                    y = tag['y'],
                    z = tag['z'],)
            else:
                tag_link.le_status =tag['le_status']
                tag_link.x = tag['x']
                tag_link.y = tag['y']
                tag_link.z = tag['z']
                tag_link.save()
                
            tag_date_link = TagDate.objects.filter(tag=tag_link).filter(time = tag['time']).first()
            if tag_date_link is None:
                TagDate.objects.create(
                    tag = tag_link,
                    time = tag['time'],
                    accuracy = tag['accuracy'],
                    kinematic = tag['kinematic'],
                    le_status = tag['le_status'],
                    motion = tag['motion'],
                    solution = tag['solution'],
                    seq = tag['seq'],
                    source = tag['source'],
                    x = tag['x'],
                    y = tag['y'],
                    z = tag['z'],)
    except Exception as err:
        logging.error(traceback.format_exc())

def update_eps_random():
    try:
        х=random.uniform(12.1, 30.0)   
        y=random.uniform(10.1, 20.0)   
        tag_link = Tag.objects.filter(sn='20005436').first()
        if tag_link is None:
                tag_link = Tag.objects.create(
                    name=tag['sn'],
                    sn=tag['sn'],
                    descr=tag['descr'],
                    origin=tag['origin'],
                    le_status =tag['le_status'],
                    x = х,
                    y = y,
                    z = 0,)
        else:
                #tag_link.le_status =tag['le_status']
                tag_link.x = х
                tag_link.y = y
                tag_link.z = 0
                tag_link.save()
                
    except Exception as err:
        logging.error(traceback.format_exc())

def update_eps_anchors():
    try:
        r=requests.post("https://192.168.10.5/CFG-API/auth",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            return
        r=requests.get("https://192.168.10.5/CFG-API/monitor/anchors",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            return
        mystr=r.json()
        for anchor in mystr['items']:
            anchor_link = Anchors.objects.filter(sn=anchor['sn']).first()
            if anchor_link is None:
                  anchor_link = Anchors.objects.create(rls_id = anchor['id'],
                                                       sn = anchor['sn'],
                                                       origin = anchor['origin'],
                                                       disabled = anchor['disabled'],
                                                       descr = anchor['descr'],
                                                       label = anchor['label'],
                                                       x = anchor['x'],
                                                       y = anchor['y'],
                                                       z = anchor['z'],
                                                       device_type = anchor['device_type'],
                                                       status = anchor['status'],
                                                       ip_address = anchor['ip_address'],
                                                       coap_resource = anchor['coap_resource'],
                                                       subscribed = anchor['subscribed'],
                                                       message_time = anchor['message_time'],
                                                       status_time = anchor['status_time'],
                                                       total_packets = anchor['total_packets'],
                                                       invalid_packets = anchor['invalid_packets'])
  

    except Exception as err:
        logging.error(traceback.format_exc())
  
def update_ops_date():
    try:
        print('start')
        mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all();
        for mfsb in mfsb_list:
            datd_mfsb = DataMfsb.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
            print(str(mfsb.date)+' '+str(mfsb.name)+'   : '+str(datd_mfsb))
            if datd_mfsb is None:
                DataMfsb.objects.create(
                    date=mfsb.date,
                    name=mfsb.name,
                    values=mfsb.values,
                    check=mfsb.check)
            mfsb.check = True
            mfsb.save()
        update_acs()
    except Exception as err:
        logging.error(traceback.format_exc())




def update_fps():
    sensor_list = FpsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsbSkpv.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    for data in data_mfsb:
        print(str(data.date)+' : '+data.name)
        sensor_link = FpsSensor.objects.filter(tag=data.name).filter(active=True).first()
        print(str(sensor_link))
        if sensor_link is not None:
            Acs_Indicators = FpsIndicators.objects.create(
                date_time =data.date,
                sensor = sensor_link,
                value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date 
            sensor_link.save()
            data.check = True
            data.save()
            print(Acs_Indicators)

def test_Mfsb_skada():
    print('Попытка подключения')
    mfsb_list = MfsbSkada.objects.using('mfsb_skada').filter(check=False).order_by('date').all()[:10];
    print('Данные получены : '+str(mfsb_list))
    print('Вывод данных ')
    for mfsb in mfsb_list:
        print(mfsb.name+'   :  '+str(mfsb.values)+'   :  '+str(mfsb.date)+'   :  '+str(mfsb.check))

def upload_code_bolid():
    file = open('code_bolid.csv', 'r')
    for line in file: 
        strLine=str(line).replace('\n','').split(';')
        code =strLine[0] 
        name =strLine[1] 
        if name =='':
            continue

        link_code=CodeBolid.objects.filter(code=code).first()
        if link_code is None:
            new_code = CodeBolid.objects.create(
                code=code,
                name=name)


def tespp():
            sensor = AcsSensor.objects.filter(id=18).first()
            critical_type = sensor.critical_type
            connect_time = sensor.connect_time
            value = sensor.value
            end_date=sensor.connect_time
            param = dict()
            param.update(sensor_type='hour')
            if param['sensor_type'] == 'sec':
                strftime = "%H:%M:%S"
                start_date = end_date - timedelta(seconds=30)
            elif param['sensor_type'] == 'min':
                strftime = "%H:%M"
                start_date = end_date - timedelta(minutes=30)
            else:
                strftime = "%H:00"
                start_date = end_date - timedelta(hours=30)
            print(str(start_date)+':'+str(end_date))
            sensor_links = AcsIndicators.objects.filter(sensor=sensor).filter(date_time__range=[start_date,end_date]).order_by('date_time').order_by('id')
            indicator_last = AcsIndicators.objects.filter(sensor=sensor).order_by('-date_time').first()
            value_last =indicator_last.value / indicator_last.sensor.ratio
            strftimeend = "%d.%m.%Y %H"
            add_true = True
            m_sensor = []
            value_old = value_last
            print(sensor_links.count())
            for i in range(31):
                if param['sensor_type'] == 'sec':
                    strftimeend = "%d.%m.%Y %H:%M:%S"
                    date_time = start_date + timedelta(seconds=i)
                elif param['sensor_type'] == 'min':
                    strftimeend = "%d.%m.%Y %H:%M"
                    date_time = start_date + timedelta(minutes=i)
                else:
                    strftimeend = "%d.%m.%Y %H"
                    date_time = start_date + timedelta(hours=i)
                sensor_dict = dict()
                sensor_dict.update(date_max=str(connect_time))
                add_true = True
                if critical_type =="max":
                    value_date =0
                else:
                    value_date =9999999
                for indicator in sensor_links:
                    indicator_date_time = indicator.date_time
                    if indicator_date_time >date_time:
                        break
                    data = indicator_date_time.strftime(strftimeend)
                    if data == date_time.strftime(strftimeend):
                        value = indicator.value / indicator.sensor.ratio
                        if critical_type =="max":
                            value_date = max(value_date,value)
                        else:
                            value_date = min(value_date,value)
                        #value = indicator.value / indicator.sensor.ratio
                        #sensor_dict.update(date_time = indicator.date_time.strftime(strftime))
                        #sensor_dict.update(value = value)
                        #sensor_dict.update(id = indicator.id)
                        add_true = False
                        #value_old = value
                        #break

                if add_true:
                    sensor_dict.update(date_time = date_time.strftime(strftime))
                    sensor_dict.update(value = value_old)
                    sensor_dict.update(id = -1)
                else:
                    sensor_dict.update(date_time = indicator_date_time.strftime(strftime))
                    sensor_dict.update(value = value_date)
                    sensor_dict.update(id = -1)

                m_sensor.append(sensor_dict)
            for sensor in m_sensor:
                print(sensor)
            #print(str(sensor.date_time)+' : '+str(sensor.value))
     #print(sensor_links.count())
     #for indicator in sensor_links:
     #    print(indicator.date_time)

if __name__ == "__main__":
    #sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    #print(sensor_list)
    #test_Mfsb()
    #update_acs()
    #update_eps()
    #update_eps_anchors()
    #while True:
    #    time.sleep(3) # ��� � 3 �������
    #    update_eps_random()

    #test_Mfsb_skada()
    #test_Mfsb2()
    #upload_code_bolid()
    #DataMfsbSkada.objects.all().delete()
    tespp()
    
