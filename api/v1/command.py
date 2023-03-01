import traceback
import requests

from requests.auth import HTTPBasicAuth

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseForbidden

from apps.catalog.models.model_positions import Position
from apps.catalog.models.model_locations import Location
from apps.catalog.models.model_departments import Department
from apps.catalog.models.model_workers import Worker
from apps.catalog.models.model_zones import Zone


from sabron.util import logging
from apps.util import generalmodule

@csrf_exempt
def tags_info():
    try:
        r=requests.post("https://192.168.10.5/CFG-API/auth",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            data=dict()
            data.update(status=-405)
            data.update(error="RTLS auth error")
            return data
        r=requests.get("https://192.168.10.5/CFG-API/monitor/tags",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            data=dict()
            data.update(status=-595)
            data.update(error="RTLS tags error")
            return data
        mystr=r.json()
        m_rags = []
        for tag in mystr['items']:
            tag_dic = dict()
            tag_dic.update(x = tag['x'])
            tag_dic.update(y = tag['y'])
            tag_dic.update(z = tag['z'])
            tag_dic.update(sn = tag['sn'])
            tag_dic.update(descr = tag['descr'])
            tag_dic.update(origin = tag['origin'])
            tag_dic.update(le_status = tag['le_status'])
            tag_dic.update(all = str(tag))
            m_rags.append(tag_dic)
        return m_rags
    except Exception as error:
        logging.error(str(traceback.format_exc()))
        data=dict()
        data.update(status=-100)
        data.update(error="system error : "+str(traceback.format_exc()))
        return data
 

@csrf_exempt
def ping():
    print('d')
    return "OK"

@csrf_exempt #Добавить платеж
def addPayment(user,data_dic): #Добавить платеж
    try:
        data=dict()
        data.update(status=0)
        data.update(error="")
        data.update(method=data_dic['method'])
        data.update(respose="OK")
        payments = data_dic['payments']
        error_list = []
        for payment in payments:
            link_workers=Workers.objects.filter(id=payment['personalaccount']).first()
            if link_workers is None:
                error_data=dict()
                error_data.update(id=payment['personalaccount'])
                error_data.update(comment=' id '+str(payment['personalaccount'])+' not found')
                error_list.append(error_data)
            date_time = datetime.strptime(payment['date_payment'], '%d-%m-%Y')
            views_account.add_payment(data_dic['id_payment'],link_workers,date_time,payment['amount'])
        data.update(id_payment=data_dic['id_payment'])
        if len(error_list) > 0:
            data.update(status=-1)
            data.update(error=error_list)
        return data
    except Exception as error:
        logging.error(str(traceback.format_exc()))
        data=dict()
        data.update(status=-100)
        data.update(error="system error : "+str(traceback.format_exc()))
        return generalmodule.ReturnJson(200,data)

@csrf_exempt #Список Подразделений
def getListDepartments(user): #Список Подразделений
    departM = []
    alldepatment=Department.objects.filter(client=user.profile.client)
    for depatment in alldepatment:
        name=depatment.name
        name=name.encode('cp1251').decode('cp1251')
        d=dict()
        d.update(id=depatment.id)
        d.update(name=name)
        departM.append(d)    
    return departM

@csrf_exempt #Список Должностей
def getListPositions(user): #Список Должностей
    positionM = []
    allposition=Positions.objects.filter(client=user.profile.client)
    for position in allposition:
        name=position.name
        name=name.encode('cp1251').decode('cp1251')
        p=dict()
        p.update(id=position.id)
        p.update(name=name)
        positionM.append(p)    
    return positionM

@csrf_exempt #Добавить сотрудника
def addWorker(user,params): #Добавить сотрудника
    name=params['lastname']+" "+params['firstName']+" "+params['middlename']
    department=Department.objects.get(id=params['department'])
    if department.client!=user.profile.client:
        data=dict()
        data.update(status=-1)
        data.update(error="department not found")
        return data

    position=Positions.objects.get(id=params['position'])
    if position.client!=user.profile.client:
        data=dict()
        data.update(status=-1)
        data.update(error="position not found")
        return data
    newWorker=Workers.objects.create(client=user.profile.client,
                           name=name,
                           lastName=params['lastname'],
                           firstName=params['firstName'],
                           otchestvo=params['middlename'],
                           sex_workers=params['sex_workers'],
                           department=department,
                           dateJob=params['dateJob'],
                           position=position,
                           idclient=params['idclient'],)
    data=dict()
    data.update(status=0)
    data.update(error="")
    respose=dict()
    respose.update(id=newWorker.id)
    respose.update(idclient=newWorker.idclient)
    data.update(respose=respose)
    return data

