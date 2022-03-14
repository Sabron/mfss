# -*- coding: utf-8 -*-
import traceback
import datetime
import requests

from datetime import datetime
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Avg, Max, Min

from apps.util import generalmodule
from sabron.util import logging


def get_ajax(request):
    try:
        data=dict()
    except Exception as err:
        logging.error(traceback.format_exc())
        data=dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

def MainIndexDefault(request):
     if request.method == "GET":
        context={
              'updatepage':True,
                }
        return render(request, 'main_index.html',context) 



@login_required(login_url='/accounts/login/?next=')
@never_cache
def MainIndex(request):
    try:
        if request.user.profile.role == 2: # Администратор системы
            return redirect('/management/')

        return MainIndexDefault(request)
    except Exception as err:
        logging.error(traceback.format_exc())
 

