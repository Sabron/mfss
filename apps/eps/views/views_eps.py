# -*- coding: utf-8 -*-
import traceback
import requests

from datetime import datetime,timedelta
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


def main_index_default(request):
     if request.method == "GET":
        context = {
                   }
        return render(request, 'eps_main.html',context) 




@login_required(login_url='/accounts/login/?next=')
@never_cache
def main_index(request):
    try:
        return main_index_default(request)
    except Exception as err:
        logging.error(traceback.format_exc())
 

