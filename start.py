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
#os.environ.setdefault("PYTHONPATH", "/home/admtime/myapp/")
django.setup() 

from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.db.models import Sum

from apps.ops.models.model_mfsb import Mfsb
from apps.main.models.model_datamfsb import DataMfsb
from apps.acs.models.model_sensor import AcsSensor
from apps.acs.models.model_indicators import AcsIndicators

from apps.eps.models.model_tags import Tag
from apps.eps.models.model_tagdates import TagDate
from apps.eps.models.model_anchors import Anchors


from django.contrib.auth.models import User





from django.conf import settings
from django.core.files import File




from datetime import datetime, timedelta, timezone



from sabron.util import logging


def update_acs():
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    print(data_mfsb)
    for data in data_mfsb:
        print(str(data.date)+' : '+data.name)
        sensor_link = AcsSensor.objects.filter(name=data.name).filter(active=True).first()
        #print(str(sensor_link))
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
        r=requests.post("https://192.168.10.5/CFG-API/auth",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            print(r.status_code)
            return
        r=requests.get("https://192.168.10.5/CFG-API/monitor/tags",auth=HTTPBasicAuth('system', 'admin'), verify=False)
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
  

def update_acs_test():
    data_mfsb = DataMfsb.objects.filter(name='MKON_SORTIROVKA.AQED_2_CO2_Otm_18000.SN_CO2_Otm_18000').filter(check=False).order_by('date').all()
    print(data_mfsb)
    for data in data_mfsb:
        print(str(data.date)+' : '+data.name)
if __name__ == "__main__":
    update_acs_test()
    #update_acs()
    #update_eps()
    #update_eps_anchors()
    #while True:
    #    time.sleep(3) # ��� � 3 �������
    #    update_eps_random()
