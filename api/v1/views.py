import traceback,json
import base64
import ast
from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.core import serializers


from apps.util import generalmodule

from users.models import Profile
from sabron.util import logging
from . import command

def user_api(request,user):
    profile=Profile.objects.filter(user=user).first()
    if not profile:
        return False;
    if profile.api_client:
        return True
    return False

def BasicAuthLoginAndPassword(auth):
    auth = auth.replace('Basic ','')
    loginAndUser=str(base64.b64decode(bytes(auth,'utf-8')).decode("utf-8")).split(":");
    return loginAndUser

#методы addworker



@csrf_exempt
def Command(request):
    """
    status:
    
        -1   - Ошибка авторизации
        -2   - Метод не найден
        -5   - Не верные параметры
        -100 - Системная ошибка
    """
    try:
        #if request.method == "POST":
        #    return redirect("/")
        #    return generalmodule.Return404()
        #data_body=json.loads(request.body)
        datadic = request.GET.dict()
        headers = request.headers
        cookies=request.COOKIES
        if 'Authorization' not in headers:
            data=dict()
            data.update(status=-1)
            data.update(error="Login incorrect!")
            return generalmodule.ReturnJson(200,data)

        loginAndUser=BasicAuthLoginAndPassword(headers['Authorization'])
        user = authenticate(username=loginAndUser[0], password=loginAndUser[1])
        if user is not None:
            if not user_api(request,user):
                data=dict()
                data.update(status=-1)
                data.update(error="The user does not have access to the api")
                return generalmodule.ReturnJson(200,data)

            if not user.is_active:
                data=dict()
                data.update(status=-1)
                data.update(error="User is not active")
                return generalmodule.ReturnJson(200,data)
        else:
            data=dict()
            data.update(status=-1)
            data.update(error="The password is valid, but the account has been disabled!")
            return generalmodule.ReturnJson(200,data)
        #Авторизовались
        if 'method' not in datadic:
            data=dict()
            data.update(status=-2)
            data.update(error="method not found")
            return generalmodule.ReturnJson(200,data)        

        data=dict()
        data.update(status=0)
        data.update(error="")
        data.update(method=datadic['method'])
        if  datadic['method']=='ping': 
            data.update(respose=command.ping())
            return generalmodule.ReturnJson(200,data)
        elif datadic['method']=='getListDepartments':  #Получить список подразделений
            data.update(respose=command.getListDepartments(user))
            return generalmodule.ReturnJson(200,data)
        elif datadic['method']=='getListPositions':  #Получить список должностей
            data.update(respose=command.getListPositions(user))
            return generalmodule.ReturnJson(200,data)
        elif datadic['method']=='getListWorkers':  #Получить список должностей
            data.update(respose=command.getListWorkers(user))
            return generalmodule.ReturnJson(200,data)
        elif datadic['method']=='anchors_info':  #Список тэгов
            data.update(respose=command.anchors_info())
            return generalmodule.ReturnJson(200,data)
        elif datadic['method']=='tags_info':  #Список тэгов
            data.update(respose=command.tags_info())
            return generalmodule.ReturnJson(200,data)
        elif datadic['method']=='tags_list':  #Список тэгов
            data.update(respose=command.tags_list(request))
            return generalmodule.ReturnJson(200,data)
        #elif datadic['method']=='addWorker':  #Получить список стран
        #    data=addWorker(user,datadic['params'])
        #    return generalmodule.ReturnJson(200,data)


        data=dict()
        data.update(status=-1)
        data.update(error="method not found")
        return generalmodule.ReturnJson(200,data)
    except Exception as error:
        logging.error(traceback.format_exc())
        data=dict()
        data.update(status=-100)
        data.update(error="system error : "+str(traceback.format_exc()))
        return generalmodule.ReturnJson(200,data)

