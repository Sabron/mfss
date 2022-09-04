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

from . import views_acs

from sabron.util import logging
from apps.util import generalmodule




@login_required(login_url='/')
@never_cache
def main_index(request):
    try:

        #if request.user.profile.role !=1 or request.user.profile.role !=2:
        #    return redirect('/')
        param=request.GET.dict()
        if 'module' in param:
            if param['module']=='acs':
                return views_acs.main_index(request)


        context = generalmodule.get_context_template()
        return render(request, 'main_management.html',context) 
    except Exception as err:
        logging.error(traceback.format_exc())
