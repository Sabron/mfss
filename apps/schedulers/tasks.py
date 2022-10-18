import traceback
import calendar
import uuid

from django.db.models import Sum

from datetime import datetime, timedelta, timezone,date

from apps.catalog.models.model_workers import Workers

from apps.ops.models.model_mfsb import Mfsb
from apps.main.models.model_datamfsb import DataMfsb
from apps.acs.models.model_sensor import AcsSensor
from apps.acs.models.model_indicators import AcsIndicators


from mfss.celery import app

from sabron.util import logging    


#def update_acs():
#    sensor_list = AcsSensor.objects.values('name').order_by('tag').distinct()
#    data_mfsb = DataMfsb.objects.filter(name__in=sensor_list).filter(check=False).order_by('date').all()
#    for data in data_mfsb:
#        sensor_link = AcsSensor.objects.filter(name=data.name).filter(active=True).first()
#        if sensor_link is not None:
#            Acs_Indicators = AcsIndicators.objects.create(
#                date_time =data.date,
#                sensor = sensor_link,
#                value = data.values)
#            sensor_link.value = data.values
#            sensor_link.save()
 #           data.check = True
 #           data.save()
 #           print(Acs_Indicators)



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
        logging.message('update_ops_date')
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
        #    update_acs()
    except Exception as err:
        logging.error(traceback.format_exc())
