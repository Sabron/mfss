import traceback
import calendar
import uuid

from django.db.models import Sum

from datetime import datetime, timedelta, timezone,date

#from apps.catalog.models.model_workersinjob import Workersinjob
#from apps.catalog.models.model_checkpoints import Checkpoints
from apps.catalog.models.model_workers import Workers
#from apps.account.models.model_personalaccounts import PersonalAccount
#from apps.catalog.models.model_subscribe_date import SubscribeDate


from hronos_school.celery import app

from sabron.util import logging    


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
