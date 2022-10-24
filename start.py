import os, django
import requests
import requests.exceptions as rex
import sys
import calendar
import uuid

import datetime as DT

from datetime import datetime, timedelta,date

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
  

if __name__ == "__main__":
    test_Mfsb()
    update_acs()
