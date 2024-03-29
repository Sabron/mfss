import traceback
import calendar
import uuid
import json
import datetime as DT
import requests
import requests.exceptions as rex

from django.db.models import Sum
from django.core.cache import cache

from requests.auth import HTTPBasicAuth

from datetime import datetime, timedelta, timezone,date


#from apps.catalog.models.model_workers import Workers

from apps.ops.models.model_mfsb import Mfsb
from apps.ops.models.model_mfsb_skada import MfsbSkada
from apps.ops.models.model_mfsb_skpv import MfsbSkpv
from apps.ops.models.model_mfsb_ppz import MfsbPpz
from apps.ops.models.model_mfsb_block import MfsbBlock
from apps.ops.models.model_mfsb_ktp import MfsbKtp

from apps.main.models.model_datamfsb import DataMfsb
from apps.main.models.model_datamfsb_ppz import DataMfsbPpz
from apps.main.models.model_datamfsb_skpv import DataMfsbSkpv
from apps.main.models.model_datamfsb_skada import DataMfsbSkada
from apps.main.models.model_dataktp import DataKtp


from apps.acs.models.model_sensor import AcsSensor
from apps.acs.models.model_indicators import AcsIndicators

from apps.ktp.models.model_sensor import KtpSensor
from apps.ktp.models.model_indicators import KtpIndicators


from apps.dcs.models.model_sensor import DcsSensor
from apps.dcs.models.model_indicators import DcsIndicators

from apps.fps.models.model_sensor import FpsSensor
from apps.fps.models.model_indicators import FpsIndicators


from apps.scada.models.model_sensor import ScadaSensor
from apps.scada.models.model_indicators import ScadaIndicators

from apps.fp.models.model_sensor import FpSensor
from apps.fp.models.model_indicators import FpIndicators
from apps.fp.models.model_code_bolid import CodeBolid

from apps.block.models.model_sensor import BlockSensor
from apps.block.models.model_indicators import BlockIndicators
from apps.block.models.model_block import Block


from apps.eps.models.model_tags import Tag
from apps.eps.models.model_tagdates import TagDate


from mfss.celery import app

from sabron.util import logging    


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

@app.task(ignore_result=True)
def update_ktp_date():# Получение данных КТП
    try:
        mfsb = cache.get('update_ktp_date')
        logging.message('update_ktp_date : '+str(mfsb))
        if not mfsb:
            cache.set('update_ktp_date', '1')
            mfsb_list = MfsbKtp.objects.using('ktp').filter(check=False).order_by('date').all()[:50000];
            bulk = []
            for mfsb in mfsb_list:
                data_ktp = DataKtp.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
                if data_ktp is None:
                    DataKtp.objects.create(
                        date=mfsb.date,
                        name=mfsb.name,
                        values=mfsb.values,
                        check=mfsb.check)
                mfsb.check = True
                bulk.append(mfsb)
                if len(bulk) > 500:
                    MfsbKtp.objects.using('ktp').bulk_update(bulk,['check'])
                    bulk = []
            MfsbKtp.objects.using('ktp').bulk_update(bulk,['check'])
            update_ktp()
            #update_dcs()
            cache.delete('update_ktp_date')
    except Exception as err:
        logging.error(traceback.format_exc())


def update_fps(): # Получение данных Системы контроля пожарного водоснабжения
    sensor_list = FpsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsbSkpv.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    for data in data_mfsb:
        sensor_link = FpsSensor.objects.filter(tag=data.name).filter(active=True).first()
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

def update_fp(): # Получение данных противопожарная защита
    sensor_list = FpSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsbPpz.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    for data in data_mfsb:
        sensor_link = FpSensor.objects.filter(tag=data.name).first()
        if sensor_link is not None:
            Acs_Indicators = FpIndicators.objects.create(
                date_time =data.date,
                sensor = sensor_link,
                code = sensor_link.code)
            code_bolid = CodeBolid.objects.filter(code=data.code).first()
            sensor_link.code = code_bolid
            sensor_link.connect_time =data.date 
            sensor_link.save()
            data.check = True
            data.save()

def update_scada(): # Получение данных Системы контроля работы оборудования
    sensor_list = ScadaSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsbSkada.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
    for data in data_mfsb:
        sensor_link = ScadaSensor.objects.filter(tag=data.name).first()
        if sensor_link is not None:
            Acs_Indicators = ScadaIndicators.objects.create(
                date_time =data.date,
                sensor = sensor_link,
                value = data.values)
            sensor_link.value = data.values
            sensor_link.connect_time =data.date 
            sensor_link.save()
            data.check = True
            data.save()


def update_acs():# Получение данных Системы Аэрогазовый контроль
    sensor_list = AcsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()[:20000]
    bulk = []
    #sensor_m=[]
    for data in data_mfsb:
        sensor_link = AcsSensor.objects.filter(tag=data.name).filter(active=True).first()
        if sensor_link is not None:
            #if sensor_link not in sensor_m:
            #    sensor_m.append(sensor_link)
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
    #for sensor in sensor_m:
    #    indicator_link = AcsIndicators.objects.filter(sensor = sensor).order_by('-date_time')[:1]
    #    if indicator_link is not None:
    #        sensor_link.value = indicator_link[0].value
    #        sensor_link.connect_time =indicator_link[0].date_time
    #       sensor_link.save()
    DataMfsb.objects.bulk_update(bulk,['check'])


def update_dcs(): # Получение данных Контроль запыленности
    sensor_list = DcsSensor.objects.values('tag').order_by('tag').distinct()
    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()[:20000]
    bulk = []
    #sensor_m=[]
    for data in data_mfsb:
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
    #for sensor in sensor_m:
    #    indicator_link = AcsIndicators.objects.filter(sensor = sensor).order_by('-date_time')[:1]
    #    if indicator_link is not None:
    #        sensor_link.value = indicator_link[0].value
    #        sensor_link.connect_time =indicator_link[0].date_time
    #        sensor_link.save()
    DataMfsb.objects.bulk_update(bulk,['check'])
 

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
        mfsb = cache.get('update_ops_date')
        if not mfsb:
            cache.set('update_ops_date', '1')
            mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all()[:20000];
            bulk = []
            for mfsb in mfsb_list:
                datd_mfsb = DataMfsb.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
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
            Mfsb.objects.using('mfsb').bulk_update(bulk,['check'])
            update_acs()
            update_dcs()
            cache.delete('update_ops_date')
    except Exception as err:
        logging.error(traceback.format_exc())

@app.task(ignore_result=True)
def update_block():
    try:
        mfsb = cache.get('mfsb_block')
        logging.message('mfsb_block : '+str(mfsb))
        if not mfsb:
            cache.set('mfsb_block', '1')
            mfsb_list = Block.objects.filter(check=False).order_by('date').all()[:50000];
            bulk = []
            for data in mfsb_list:
                block_sensor = BlockSensor.objects.filter(tag = data.name).first()
                if block_sensor is None:
                    block_sensor = BlockSensor.objects.create(
                                tag = data.name,
                                position = 'None',
                                name = data.name)

                indicator_link = BlockIndicators.objects.filter(sensor = block_sensor).filter(date_time__lte=data.date).order_by('-date_time')[:1]
                if indicator_link.count() > 0 :
                    if int(indicator_link[0].value) != int(data.values):
                        Acs_Indicators = BlockIndicators.objects.create(
                            date_time =data.date,
                            sensor = block_sensor,
                            value = int(data.values))
                else:
                    Acs_Indicators = BlockIndicators.objects.create(
                        date_time =data.date,
                        sensor = block_sensor,
                        value = int(data.values))
                block_sensor.value = int(data.values)
                block_sensor.connect_time =data.date
                block_sensor.save()
                data.check = True
                #data.save()
                bulk.append(data)
                if len(bulk) >= 500:
                    Block.objects.bulk_update(bulk,['check'])
                    bulk = []
            Block.objects.bulk_update(bulk,['check'])
            Block.objects.filter(check=True).delete();
            cache.delete('mfsb_block')
    except Exception as err:
        logging.error("==============update_block")
        logging.error(traceback.format_exc())

@app.task(ignore_result=True)
def update_ops_skpv_date():
    try:
        mfsb = cache.get('update_ops_skpv_date')
        logging.message('update_ops_skpv_date : '+str(mfsb))
        if not mfsb:
            cache.set('update_ops_skpv_date', '1')
            mfsb_list = MfsbSkpv.objects.using('mfsb_skpv').filter(check=False).order_by('date').all()[:5000];
            count_d = 0
            for mfsb in mfsb_list:
                datd_mfsb = DataMfsbSkpv.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
                if datd_mfsb is None:
                    DataMfsbSkpv.objects.create(
                        date=mfsb.date,
                        name=mfsb.name,
                        values=mfsb.values,
                        check=mfsb.check)
                else:
                    count_d = count_d+1
                mfsb.check = True
                mfsb.save()
            #logging.message(str(count_d)+' / 5000')
            update_fps()
            cache.delete('update_ops_skpv_date')
    except Exception as err:
        logging.error(traceback.format_exc())

@app.task(ignore_result=True)
def update_ops_ppz_date():
    try:
        mfsb = cache.get('update_ops_ppz_date')
        if not mfsb:
            cache.set('update_ops_ppz_date', '1')
            mfsb_list = MfsbPpz.objects.using('mfsb_ppz').filter(check=False).order_by('date').all()[:5000];
            count_d = 0
            for mfsb in mfsb_list:
                datd_mfsb = DataMfsbPpz.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
                if datd_mfsb is None:
                    DataMfsbPpz.objects.create(
                        date=mfsb.date,
                        name=mfsb.name,
                        code=mfsb.code,
                        check=mfsb.check)
                else:
                    count_d = count_d+1

                code_bolid = CodeBolid.objects.filter(code=mfsb.code).first()
                link_sensor = FpSensor.objects.filter(tag=mfsb.name).first()
                if link_sensor is None:
                    FpSensor.objects.create(
                        tag=mfsb.name,
                        name=mfsb.name,
                        code = code_bolid,
                        active=False)
 
                mfsb.check = True
                mfsb.save()
            update_fp()
            cache.delete('update_ops_ppz_date')
    except Exception as err:
        logging.error(traceback.format_exc())

@app.task(ignore_result=True)
def update_ops_scada_date():
    try:
        mfsb = cache.get('update_ops_scada_date')
        logging.message('scada : '+str(mfsb))
        if not mfsb:
            cache.set('update_ops_scada_date', '1')
            mfsb_list = MfsbSkada.objects.using('mfsb_skada').filter(check=False).order_by('date').all()[:5000];
            count_d = 0
            for mfsb in mfsb_list:
                datd_mfsb = DataMfsbSkada.objects.filter(date=mfsb.date).filter(name=mfsb.name).first()
                if datd_mfsb is None:
                    DataMfsbSkada.objects.create(
                        date=mfsb.date,
                        name=mfsb.name,
                        values=mfsb.values,
                        check=mfsb.check)
                else:
                    count_d = count_d+1

                link_sensor = ScadaSensor.objects.filter(tag=mfsb.name).first()
                if link_sensor is None:
                    ScadaSensor.objects.create(
                        tag=mfsb.name,
                        name=mfsb.name,
                        value=mfsb.values,
                        active=False)
                mfsb.check = True
                mfsb.save()
            update_scada()
            cache.delete('update_ops_scada_date')
    except Exception as err:
        logging.error(traceback.format_exc())


@app.task(ignore_result=True)
def auto_ops_delete():
    try:
        MfsbSkpv.objects.using('mfsb_skpv').filter(check=True).delete();
        Mfsb.objects.using('mfsb').filter(check=True).delete();
        MfsbPpz.objects.using('mfsb_ppz').filter(check=True).delete();
        MfsbSkada.objects.using('mfsb_skada').filter(check=True).delete();
        MfsbBlock.objects.using('mfsb_block').filter(check=True).delete();
        MfsbKtp.objects.using('ktp').filter(check=True).delete();
    except Exception as err:
        logging.error(traceback.format_exc())





@app.task(ignore_result=True)
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
