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

from django.contrib.auth.models import User





from django.conf import settings
from django.core.files import File




from datetime import datetime, timedelta, timezone



from sabron.util import logging



def test_Mfsb():
    mfsb_list = Mfsb.objects.using('mfsb').filter(check=False).order_by('date').all();
    for mfsb in mfsb_list:
        print(mfsb.name+'   :  '+str(mfsb.values))
    #mfsb_list = Mfsb.objects.using('mfsb').values('name').filter(check=False).distinct()
    #for mfsb in mfsb_list:
    #    print(mfsb['name'])
    


if __name__ == "__main__":
    test_Mfsb()
