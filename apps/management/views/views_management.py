# -*- coding: utf-8 -*-
import traceback
import os
import io
import json


from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User

from sabron.util import logging

from apps.util import generalmodule




@login_required(login_url='/')
@never_cache
def main_index(request):
    try:
        if request.method == "GET":
            context = generalmodule.get_context_template()
            return render(request, 'main_management.html',context) 
    except Exception as err:
        logging.error(traceback.format_exc())
