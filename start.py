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
from dateutil import tz
from tqdm import tqdm

from datetime import datetime, timedelta,date
from requests.auth import HTTPBasicAuth
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mfss.settings')
django.setup() 

from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.db.models import Sum
from django.db.models import Max,Min
from django.db import connection
from django.core.cache import cache

from apps.ops.models.model_mfsb import Mfsb
from apps.ops.models.model_mfsb_skada import MfsbSkada
from apps.ops.models.model_mfsb_ppz import MfsbPpz
from apps.ops.models.model_mfsb_skpv import MfsbSkpv
from apps.ops.models.model_mfsb_block import MfsbBlock
from apps.ops.models.model_mfsb_ktp import MfsbKtp


from apps.main.models.model_datamfsb import DataMfsb
from apps.main.models.model_datamfsb_skada import DataMfsbSkada
from apps.main.models.model_datamfsb_ppz import DataMfsbPpz
from apps.main.models.model_datamfsb_skpv import DataMfsbSkpv
from apps.main.models.model_dataktp import DataKtp

from apps.ktp.models.model_sensor import KtpSensor
from apps.ktp.models.model_indicators import KtpIndicators


from apps.acs.models.model_sensor import AcsSensor
from apps.acs.models.model_indicators import AcsIndicators

from apps.dcs.models.model_sensor import DcsSensor
from apps.dcs.models.model_indicators import DcsIndicators


from apps.fps.models.model_sensor import FpsSensor
from apps.fps.models.model_indicators import FpsIndicators


from apps.fp.models.model_sensor import FpSensor
from apps.fp.models.model_indicators import FpIndicators

from apps.scada.models.model_indicators import ScadaIndicators


from apps.block.models.model_sensor import BlockSensor
from apps.block.models.model_indicators import BlockIndicators
from apps.block.models.model_block import Block


from apps.eps.models.model_tags import Tag
from apps.eps.models.model_tagdates import TagDate
from apps.eps.models.model_anchors import Anchors

from apps.fp.models.model_code_bolid import CodeBolid

from django.contrib.auth.models import User





from django.conf import settings
from django.core.files import File




from datetime import datetime, timedelta, timezone



from sabron.util import logging


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
            sensor = AcsSensor.objects.filter(id=11).first()
            critical_type = sensor.critical_type
            connect_time = sensor.connect_time
            value = sensor.value
            end_date=sensor.connect_time
            param = dict()
            param.update(sensor_type='sec')
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
            #indicator_last = AcsIndicators.objects.filter(sensor=sensor).order_by('-date_time').first()
            #value_last =indicator_last.value / indicator_last.sensor.ratio
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
            for sensor in m_sensor:
                print(sensor)
            #print(str(sensor.date_time)+' : '+str(sensor.value))
     #print(sensor_links.count())
     #for indicator in sensor_links:
     #    print(indicator.date_time)

def test_idicator():
    sensor_link = AcsSensor.objects.filter(id=13).first()
    indicator_link = AcsIndicators.objects.filter(sensor = sensor_link).order_by('date_time')[:1]
    print(indicator_link.count())
    if indicator_link[0].value != 48:
        print(indicator_link)
        print(indicator_link[0].date_time)
        print(indicator_link[0].value)

def test_update_acs():
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).order_by('date').all()
    count = data_mfsb.count()
    print('Обработано : '+str(0)+' из '+str(count))
    for data in tqdm(data_mfsb):
        sensor_link = AcsSensor.objects.filter(tag=data.name).filter(active=True).first()
        if sensor_link is not None:
            indicator_link = AcsIndicators.objects.filter(sensor = sensor_link).filter(date_time__lte=data.date).order_by('date_time')[:1]
            if indicator_link.count() > 0 :
                if indicator_link[0].value != data.values:
                    Acs_Indicators = AcsIndicators.objects.create(
                        date_time =data.date,
                        sensor = sensor_link,
                        value = data.values)
            else:
                Acs_Indicators = AcsIndicators.objects.create(
                    date_time =data.date,
                    sensor = sensor_link,
                   value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date
            sensor_link.save()
            data.check = True
            data.save()
    print('OK')  

def delete_data():
    Data_Mfsb = DataMfsb.objects.filter(date__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    DataMfsb_Skada = DataMfsbSkada.objects.filter(date__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    DataMfsb_Ppz = DataMfsbPpz.objects.filter(date__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    DataMfsb_Skpv = DataMfsbSkpv.objects.filter(date__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    Acs_Indicators = AcsIndicators.objects.filter(date_time__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    Dcs_Indicators = DcsIndicators.objects.filter(date_time__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    Fp_Indicators = FpIndicators.objects.filter(date_time__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    Fps_Indicators = FpsIndicators.objects.filter(date_time__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()
    Scada_Indicators = ScadaIndicators.objects.filter(date_time__lte=DT.datetime(2022, 12, 31,0,0,0)).delete()

    MfsbSkpv.objects.using('mfsb_skpv').filter(check=True).delete();
    Mfsb.objects.using('mfsb').filter(check=True).delete();
    MfsbPpz.objects.using('mfsb_ppz').filter(check=True).delete();
    MfsbSkada.objects.using('mfsb_skada').filter(check=True).delete();


def len_data():
    Data_Mfsb = DataMfsb.objects.all()
    DataMfsb_Skada = DataMfsbSkada.objects.all()
    DataMfsb_Ppz = DataMfsbPpz.objects.all()
    DataMfsb_Skpv = DataMfsbSkpv.objects.all()
    Acs_Indicators = AcsIndicators.objects.all()
    Dcs_Indicators = DcsIndicators.objects.all()
    Fp_Indicators = FpIndicators.objects.all()
    Fps_Indicators = FpsIndicators.objects.all()
    Scada_Indicators = ScadaIndicators.objects.all()
    Mfsb_l = Mfsb.objects.using('mfsb').all()
    MfsbSkpv_l = MfsbSkpv.objects.using('mfsb_skpv').all()
    MfsbPpz_l = MfsbPpz.objects.using('mfsb_ppz').all()
    MfsbSkada_l = MfsbSkada.objects.using('mfsb_skada').all()

    print(' Mfsb = '+str(Mfsb_l.count()))
    print(' MfsbSkpv = '+str(MfsbSkpv_l.count()))
    print(' MfsbPpz = '+str(MfsbPpz_l.count()))
    print(' MfsbSkada = '+str(MfsbSkada_l.count()))

    print(' DataMfsb = '+str(Data_Mfsb.count()))
    print(' DataMfsbSkada = '+str(DataMfsb_Skada.count()))
    print(' DataMfsbPpz = '+str(DataMfsb_Ppz.count()))
    print(' DataMfsbSkpv = '+str(DataMfsb_Skpv.count()))
    print(' AcsIndicators = '+str(Acs_Indicators.count()))
    print(' DcsIndicators = '+str(Dcs_Indicators.count()))
    print(' FpIndicators = '+str(Fp_Indicators.count()))
    print(' FpsIndicators = '+str(Fps_Indicators.count()))
    print(' ScadaIndicators = '+str(Scada_Indicators.count()))

def update_acs():# Получение данных Системы Аэрогазовый контроль
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    print('update acs : '+str(len(sensor_list)))
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()[:50000]
    print('update_acs : '+str(data_mfsb.count()))
    bulk = []
    sensor_m=[]
    for data in tqdm(data_mfsb):
        sensor_link = AcsSensor.objects.filter(tag=data.name).filter(active=True).first()
        if sensor_link is not None:
            if sensor_link not in sensor_m:
                sensor_m.append(sensor_link)
            indicator_link = AcsIndicators.objects.filter(sensor = sensor_link).filter(date_time__lte=data.date).order_by('-date_time')[:1]
            if indicator_link.count() > 0 :
                if indicator_link[0].value != data.values:
                    Acs_Indicators = AcsIndicators.objects.create(
                        date_time =data.date,
                        sensor = sensor_link,
                        value = data.values)
            else:
                Acs_Indicators = AcsIndicators.objects.create(
                    date_time =data.date,
                    sensor = sensor_link,
                    value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date
            sensor_link.save()
            data.check = True
            #data.save()
            bulk.append(data)
            if len(bulk) > 500:
                DataMfsb.objects.bulk_update(bulk,['check'])
                bulk = []

    print('Обновляем последнее значение')
    for sensor in sensor_m:
        indicator_link = AcsIndicators.objects.filter(sensor = sensor).order_by('-date_time')[:1]
        if indicator_link is not None:
            print(str(sensor)+' : '+str(indicator_link[0].date_time))
            sensor_link.value = indicator_link[0].value
            sensor_link.connect_time =indicator_link[0].date_time
            sensor_link.save()
    DataMfsb.objects.bulk_update(bulk,['check'])

def update_acs_one(sensor_link):# Получение данных Системы Аэрогазовый контроль
    #sensor_link = AcsSensor.objects.get(id=id)
    data_mfsb = DataMfsb.objects.filter(name=sensor_link.tag).filter(check=False).order_by('date').all()[:50000]
    print('update_acs : '+str(data_mfsb.count()))
    bulk = []
    for data in tqdm(data_mfsb):
            indicator_link = AcsIndicators.objects.filter(sensor = sensor_link).filter(date_time__lte=data.date).order_by('-date_time')[:1]
            if indicator_link.count() > 0 :
                if indicator_link[0].value != data.values:
                    Acs_Indicators = AcsIndicators.objects.create(
                        date_time =data.date,
                        sensor = sensor_link,
                        value = data.values)
            else:
                Acs_Indicators = AcsIndicators.objects.create(
                    date_time =data.date,
                    sensor = sensor_link,
                    value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date
            sensor_link.save()
            data.check = True
            bulk.append(data)
            if len(bulk) > 500:
                DataMfsb.objects.bulk_update(bulk,['check'])
                bulk = []
    DataMfsb.objects.bulk_update(bulk,['check'])

def update_dcs(): # Получение данных Контроль запыленности
    sensor_list = DcsSensor.objects.values('tag').order_by('tag').distinct()
    print('update dcs : '+str(len(sensor_list)))
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()[:50000]
    bulk = []
    #sensor_m=[]
    for data in tqdm(data_mfsb):
        sensor_link = DcsSensor.objects.filter(tag=data.name).filter(active=True).first()
        if sensor_link is not None:
            #if sensor_link not in sensor_m:
            #    sensor_m.append(sensor_link)
            Acs_Indicators = DcsIndicators.objects.create(
                date_time =data.date,
                sensor = sensor_link,
                value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date
            sensor_link.save()
            data.check = True
            #data.save()
            bulk.append(data)
            if len(bulk) > 500:
                DataMfsb.objects.bulk_update(bulk,['check'])
                bulk = []

    #print('Обновляем последнее значение')
    #for sensor in sensor_m:
    #    indicator_link = DcsIndicators.objects.filter(sensor = sensor).order_by('-date_time')[:1]
    #    if indicator_link is not None:
    #        print(str(sensor)+' : '+str(indicator_link[0].date_time))
    #        sensor_link.value = indicator_link[0].value
    #        sensor_link.connect_time =indicator_link[0].date_time
    #        sensor_link.save()
    DataMfsb.objects.bulk_update(bulk,['check'])


def update_ops_date():
    try:
        data_mfsb = DataMfsb.objects.filter(check=False).order_by('date').all()
        print('data_mfsb = '+str(data_mfsb.count()))
        mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all();
        print('mfsb_list = '+str(mfsb_list.count()))
        mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all()[:50000];
        print('mfsb_list = '+str(mfsb_list.count()))
        bulk = []
        for mfsb in tqdm(mfsb_list):
            datd_mfsb = DataMfsb.objects.filter(date=mfsb.date).filter(name=mfsb.name).order_by('date').first()
            #datd_mfsb = DataMfsb.objects.filter(date__lte=mfsb.date).filter(name=mfsb.name).order_by('date').first()
            if datd_mfsb is None:
                DataMfsb.objects.create(
                    date=mfsb.date,
                    name=mfsb.name,
                    values=mfsb.values,
                    check=mfsb.check)
            mfsb.check = True
            bulk.append(mfsb)
            if len(bulk) > 500:
                Mfsb.objects.using('mfsb').bulk_update(bulk,['check'])
                bulk = []
        print('Помечаем обработанные')
        Mfsb.objects.using('mfsb').bulk_update(bulk,['check'])
        print('Удаляем обработанные')
        Mfsb.objects.using('mfsb').filter(check=True).delete();
        print('Смотрим на старые')
        mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all()[:1];
        for mfsb in mfsb_list:
            print(str(mfsb.date))
        update_acs()
        update_dcs()
    except Exception as err:
        logging.error("==============update_ops_date")
        logging.error(traceback.format_exc())


def update_block():
    try:
            print(Block.objects.count())
            mfsb_list = Block.objects.filter(check=False).order_by('date').all()[:50000];
            bulk = []
            for data in tqdm(mfsb_list):
                block_sensor = BlockSensor.objects.filter(tag = data.name).first()
                if block_sensor is None:
                    block_sensor = BlockSensor.objects.create(
                                tag = data.name,
                                position = 'None',
                                name = data.name)

                indicator_link = BlockIndicators.objects.filter(sensor = block_sensor).filter(date_time__lte=data.date).order_by('-date_time')[:1]
                if indicator_link.count() > 0 :
                    if indicator_link[0].value != data.values:
                        Acs_Indicators = BlockIndicators.objects.create(
                            date_time =data.date,
                            sensor = block_sensor,
                            value = data.values)
                else:
                    Acs_Indicators = BlockIndicators.objects.create(
                        date_time =data.date,
                        sensor = block_sensor,
                        value = data.values)
                block_sensor.value = data.values
                block_sensor.connect_time =data.date
                block_sensor.save()
                data.check = True
                #print('Запись')
                #data.save() 
                bulk.append(data)
                if len(bulk) >= 500:
                    Block.objects.bulk_update(bulk,['check'])
                    bulk = []
            print('Помечаем')
            Block.objects.bulk_update(bulk,['check'])
            print('Удаляем')
            Block.objects.filter(check=True).delete();
    except Exception as err:
        logging.error("==============update_block")
        logging.error(traceback.format_exc())

def test_Mfsb_block():
    MfsbBlock.objects.using('mfsb_block').filter(date__lte=DT.datetime(1601, 12, 1,0,0,0)).delete()
    Mfsb_Block = MfsbBlock.objects.using('mfsb_block').filter(check=False).all();
    print(Mfsb_Block.count())
    
    #print('Попытка подключения')
    #mfsb_list = MfsbBlock.objects.using('mfsb_block').filter(check=False).order_by('date').all()[:10];
    #print('Данные получены : '+str(mfsb_list.count()))

def control_sensor():
    data_mfsb = DataMfsb.objects.values('name').order_by('name').distinct()
    for sensor in data_mfsb:
        print(sensor['name'])
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    print('update acs : '+str(len(sensor_list)))
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()[:50000]
    print('data_mfsb = '+str(data_mfsb.count()))


def delete_acsIndicator():
    all_in = AcsIndicators.objects.all()
    old = all_in.count()
    print('Записей : '+str(old))
    sensor_list = AcsSensor.objects.order_by('id').all()
    for sensor in sensor_list:
        print(sensor)
        old_value = 9999999.9
        allindicator = AcsIndicators.objects.filter(sensor = sensor).order_by('date_time').all()
        for indicator in tqdm(allindicator):
            #print(str(indicator.date_time)+' : '+str(indicator.value)+' : '+str(indicator.ismarked))
            if old_value == 9999999.9:
               old_value = indicator.value
            else:
                if old_value != indicator.value:
                    old_value = indicator.value
                else:
                    indicator.ismarked = True
                    indicator.save()
        AcsIndicators.objects.filter(ismarked = True).delete()
        #all_in = AcsIndicators.objects.all()
        #new = all_in.count()
        #print('Удалено : '+str(old-new))
        #print('Осталось : '+str(new))
        #break
    AcsIndicators.objects.filter(ismarked = True).delete()
    all_in = AcsIndicators.objects.all()
    new = all_in.count()
    print('Удалено : '+str(old-new))
    print('Осталось : '+str(new))


def update_ktp_date():# Получение данных КТП
    try:
        #mfsb = cache.get('update_ktp_date')
        #if not mfsb:
        #    cache.set('update_ktp_date', '1')
            mfsb_list = MfsbKtp.objects.using('ktp').filter(check=False).order_by('date').all()[:200000];
            bulk = []
            for mfsb in tqdm(mfsb_list):
                data_ktp = DataKtp.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
                if data_ktp is None:
                    DataKtp.objects.create(
                        date=mfsb.date,
                        name=mfsb.name,
                        values=mfsb.values,
                        check=mfsb.check)
                #mfsb.check = True
                #bulk.append(mfsb)
                #if len(bulk) > 500:
                #    MfsbKtp.objects.using('ktp').bulk_update(bulk,['check'])
                #    bulk = []
            #MfsbKtp.objects.using('ktp').bulk_update(bulk,['check'])
            #update_acs()
            #update_dcs()
         #   cache.delete('update_ktp_date')
    except Exception as err:
        logging.error(traceback.format_exc())

def update_ktp():# Обработка данных КТП
    try:
        bulk = []
        data_ktp= DataKtp.objects.filter(check=False).order_by('date').all()[:20000]
        for data in data_ktp:
            serial = data.values[0:3]
            sensor_link = KtpSensor.objects.filter(tag=data.name).first()
            if sensor_link is None:
                sensor_link = KtpSensor.objects.create(
                    tag = data.name,
                    name = data.name,
                    serial = serial,
                    connect_time = data.date) 
            else:
                sensor_link.connect_time = data.date
                sensor_link.serial = serial
                sensor_link.save()
            if 'Показания Активная + Реактивная ЭЭ Т1' in data.name:
                if '282' in serial:
                    value_akt = data.values[5:15]
                    value_reakt = data.values[15:len(data.values)]
                    #print('Показания Активная + Реактивная ЭЭ Т1 : '+data.values)
                    #print('Время : '+str(data.date))
                    #print('Активная : '+value_akt)
                    #print('Реактивная : '+value_reakt)
                    indicator_link = KtpIndicators.objects.filter(sensor = sensor_link).filter(date_time=data.date).first()
                    if indicator_link is None:
                        KtpIndicators.objects.create(sensor = sensor_link,
                                                     date_time = data.date,
                                                     value_akt = value_akt,
                                                     value_reakt = value_reakt)
                    else:
                        indicator_link.value_akt = value_akt
                        indicator_link.value_reakt = value_reakt
                        indicator_link.save()
                    data.check = True
                    bulk.append(data)
                    if len(bulk) > 500:
                        DataKtp.objects.bulk_update(bulk,['check'])
                        bulk = []
            if 'Показания Активная + Реактивная ЭЭ Т2' in data.name:
               if '282' in serial:
                    value_akt = data.values[5:15]
                    value_reakt = data.values[15:len(data.values)]
                    #print('Показания Активная + Реактивная ЭЭ Т2 : '+data.values)
                    #print('Время : '+str(data.date))
                    #print('Активная : '+value_akt)
                    #print('Реактивная : '+value_reakt)
                    indicator_link = KtpIndicators.objects.filter(sensor = sensor_link).filter(date_time=data.date).first()
                    if indicator_link is None:
                        KtpIndicators.objects.create(sensor = sensor_link,
                                                     date_time = data.date,
                                                     value_akt = value_akt,
                                                     value_reakt = value_reakt)
                    else:
                        indicator_link.value_akt = value_akt
                        indicator_link.value_reakt = value_reakt
                        indicator_link.save()
                    data.check = True
                    bulk.append(data)
                    if len(bulk) > 500:
                        DataKtp.objects.bulk_update(bulk,['check'])
                        bulk = []

            if 'Показания Активная ЭЭ Т1' in data.name:
                #print('Показания Активная ЭЭ Т1 : ')
                pass
            if 'Показания Активная ЭЭ Т2' in data.name:
                #print('Показания Активная ЭЭ Т2 : ')
                pass
        DataKtp.objects.bulk_update(bulk,['check'])
    except Exception as err:
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    update_ktp()
    #for i in range(1, 200):
    #    print('**************')
    #    print('* Итерация : '+str(i))
    #    print('**************')
        
    #update_block();
    #len_data()
    #delete_data()
    #len_data()
    #test_Mfsb_block()
    #sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    #for sensor in sensor_list:
    #    sensor_link = AcsSensor.objects.filter(tag=sensor['tag']).filter(active=True).first()
    #    indicator_link = AcsIndicators.objects.filter(sensor = sensor_link).order_by('-date_time')[:1]
    #    if indicator_link.count() > 0:
    #        print(str(sensor_link)+' : '+str(indicator_link[0].date_time))
    #        sensor_link.value = indicator_link[0].value
    #        sensor_link.connect_time =indicator_link[0].date_time
    #        sensor_link.save()
    #for i in range(1, 200):
    #    test_Mfsb_block()
    #    update_block()
    #control_sensor()
    #DataMfsb.objects.filter(check=True).delete()
    #for i in range(1, 200):
    #    DataMfsb.objects.filter(check=True).delete()
    #    print('**************')
    #    print('* Итерация : '+str(i))
    #    print('**************')
    #    update_ops_date()
        #update_acs_one()
        #MKON_BUNKER1.AQED_19_METAN_Otm_10700.Metan_Otm_10700
        #sensor_link = AcsSensor.objects.get(id=12)
        #print(sensor_link)
        #allindicator = AcsIndicators.objects.filter(sensor = sensor_link).all()
        #print(allindicator.count())
        #dd = DataMfsb.objects.filter(name='MKON_BUNKER1.AQED_19_METAN_Otm_10700.Metan_Otm_10700').all()
        #print(dd.count())
    #DataMfsb.objects.filter(check=True).delete()




    #sensor_list = AcsSensor.objects.order_by('id').all()
    #for sensor in sensor_list:
        #sensor = AcsSensor.objects.get(id=12)
    #    allindicator = AcsIndicators.objects.filter(sensor = sensor).all()
    #    print(str(sensor) + ' : '+str(allindicator.count()))
    #    data_mfsb = DataMfsb.objects.filter(check=False).order_by('date').all()
    #    print('data_mfsb = '+str(data_mfsb.count()))
    #    print(sensor)
    #    update_acs_one(sensor)
    #    DataMfsb.objects.filter(check=True).delete()

    #    sensor = AcsSensor.objects.get(id=12)
    #    datete_list = AcsIndicators.objects.filter(sensor=sensor).values('value').distinct()
    #    print(len(datete_list))
        #DataMfsb.objects.filter(check=True).delete()
        #data_mfsb = DataMfsb.objects.filter(name=sensor.tag).filter(check=False).order_by('date').all()[:1]
        #print('update_acs : '+str(data_mfsb.count()))
        #bulk = []
        #sensor_m=[]
        #sensor_m.append(sensor)
        #date_m = []
        #for data in tqdm(data_mfsb):
        #    indicator_link = AcsIndicators.objects.filter(sensor=sensor).filter(date_time__lte=data.date).order_by('-date_time').first()
            
        #    print(connection.queries)
        #    if indicator_link is not None:
        #        if data.date not in date_m:
        #            date_m.append(data.date)
        #print(len(date_m))
        #for dd in date_m:
        #    print(dd)