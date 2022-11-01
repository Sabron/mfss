import os, django
import requests
import requests.exceptions as rex
import sys
import calendar
import uuid
import datetime as DT
import pytz
import json
import maya
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


from django.contrib.auth.models import User





from django.conf import settings
from django.core.files import File




from datetime import datetime, timedelta, timezone



from sabron.util import logging


def update_acs():
    sensor_list = AcsSensor.objects.values('name').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
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
            return
        r=requests.get("https://192.168.10.5/CFG-API/monitor/tags",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            return
        mystr=r.json()
        for tag in mystr['items']:
            timezone_date_time_obj = maya.parse(tag['time']).datetime(to_timezone='Europe/Moscow', naive=False)
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

  

if __name__ == "__main__":
    #test_Mfsb()
    #update_acs()
    update_eps()
    #while True:
    #    time.sleep(3) # ��� � 3 �������
    #    update_eps_random()
