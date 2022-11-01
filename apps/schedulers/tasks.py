import traceback
import calendar
import uuid
import json
import datetime as DT
import requests
import requests.exceptions as rex

from django.db.models import Sum
from requests.auth import HTTPBasicAuth

from datetime import datetime, timedelta, timezone,date


#from apps.catalog.models.model_workers import Workers

from apps.ops.models.model_mfsb import Mfsb
from apps.main.models.model_datamfsb import DataMfsb
from apps.acs.models.model_sensor import AcsSensor
from apps.acs.models.model_indicators import AcsIndicators

from apps.eps.models.model_tags import Tag
from apps.eps.models.model_tagdates import TagDate


from mfss.celery import app

from sabron.util import logging    


def update_acs():
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    for data in data_mfsb:
        sensor_link = AcsSensor.objects.filter(tag=data.name).filter(active=True).first()
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
 

def end_moth(old_date,mes):
    if old_date is None:
        dt = datetime.now()
    else:
        dt = old_date
    result = dt # - timedelta(days=5)
    days_in_month = calendar.monthrange(dt.year, dt.month)[1]
    dt = result
    for i in range(1, mes):
        dt = dt+ timedelta(days=days_in_month) 	
        days_in_month = calendar.monthrange(dt.year, dt.month)[1]
        if dt.month == 6:
            dt = dt+ timedelta(days=30) 	
        if dt.month == 7:
            dt = dt+ timedelta(days=31) 	
        if dt.month == 8:
            dt = dt+ timedelta(days=31) 	

    dt = dt+ timedelta(days=days_in_month) 	
    days_in_month = calendar.monthrange(dt.year, dt.month)[1]
    return dt


@app.task(ignore_result=True)
def auto_checkin():
    try:
        pass
    except Exception as err:
        logging.error(traceback.format_exc())
        return HttpResponse("ERROR", content_type="text/plain")
    

@app.task(ignore_result=True)
def update_subscribe_payment():
    try:
        pass
    except Exception as err:
        logging.error(traceback.format_exc())
        return HttpResponse("ERROR", content_type="text/plain")


@app.task(ignore_result=True)
def update_ops_date():
    try:
        mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all();
        for mfsb in mfsb_list:
            datd_mfsb = DataMfsb.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
            if datd_mfsb is None:
                DataMfsb.objects.create(
                    date=mfsb.date,
                    name=mfsb.name,
                    values=mfsb.values,
                    check=mfsb.check)
            mfsb.check = True
            mfsb.save()
        update_acs()
        #Mfsb.objects.using('mfsb').filter(check=True).delete()
    except Exception as err:
        logging.error(traceback.format_exc())

@app.task(ignore_result=True)
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
