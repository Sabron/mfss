import traceback
import requests

from requests.auth import HTTPBasicAuth

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseForbidden
from django.db.models import Q

from apps.catalog.models.model_positions import Position
from apps.catalog.models.model_locations import Location
from apps.catalog.models.model_departments import Department
from apps.catalog.models.model_workers import Worker
from apps.catalog.models.model_zones import Zone
from apps.eps.models.model_tagdates import TagDate
from apps.eps.models.model_tags import Tag

from sabron.util import logging
from apps.util import generalmodule

@csrf_exempt
def anchors_info():
    try:
        r=requests.post("https://192.168.10.5/CFG-API/auth",auth=HTTPBasicAuth('system', 'admin'), verify=False)
        if r.status_code!=200:
            data=dict()
            data.update(status=-405)
            data.update(error="RTLS auth error")
            return data
        r=requests.get("https://192.168.10.5/CFG-API/monitor/anchors",auth=HTTPBasicAuth('system', 'admin'), verify=False)
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
            tag_dic.update(status = tag['status'])
            tag_dic.update(label = tag['label'])
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
def tags_list(request):
    try:
        param = request.GET.dict()
        m_tags_list = []
        if 'tag' in param:
            tag_link = Tag.objects.filter(sn=param['tag']).first()
            if tag_link is None:
                return m_tags_list;
            if 'datastart' in param and 'datastop' in param:
                data_start=datetime.strptime(param['datastart']+' 00:00:00', "%d-%m-%Y %H:%M:%S")
                data_stop=datetime.strptime(param['datastop']+' 23:59:59', "%d-%m-%Y %H:%M:%S")
                myquery =Q(tag = tag_link)
                myquery &= Q(time__range=[data_start,data_stop])
                tagdate_list = TagDate.objects.filter(myquery).order_by('time').all()
                for tagdate in tagdate_list:
                    tag_dic = dict()
                    tag_dic.update(tag = str(tag_link.sn))
                    tag_dic.update(time = str(tagdate.time))    
                    tag_dic.update(accuracy = tagdate.accuracy)
                    tag_dic.update(kinematic = tagdate.kinematic)
                    tag_dic.update(seq = tagdate.seq)
                    tag_dic.update(source = tagdate.source)
                    tag_dic.update(le_status = tagdate.le_status)
                    tag_dic.update(motion = tagdate.motion)
                    tag_dic.update(solution = tagdate.solution)
                    tag_dic.update(x = tagdate.x)
                    tag_dic.update(y = tagdate.y)
                    tag_dic.update(z = tagdate.z)
                    m_tags_list.append(tag_dic)
                return m_tags_list
            if 'date' in param and 'time' in param: 
                split_date = param['date'].split('-')
                split_time = param['time'].split(':')
                data_start=datetime.strptime(param['date']+' '+param['time']+'.000000', "%d-%m-%Y %H:%M:%S.%f")
                data_stop=datetime.strptime(param['date']+' '+param['time']+'.999999', "%d-%m-%Y %H:%M:%S.%f")
                myquery =Q(tag = tag_link)
                myquery &= Q(time__range=[data_start,data_stop])
                tagdate_list = TagDate.objects.filter(myquery).order_by('time').all()
                for tagdate in tagdate_list:
                    tag_dic = dict()
                    tag_dic.update(tag = str(tag_link.sn))
                    tag_dic.update(time = str(tagdate.time))    
                    tag_dic.update(accuracy = tagdate.accuracy)
                    tag_dic.update(kinematic = tagdate.kinematic)
                    tag_dic.update(seq = tagdate.seq)
                    tag_dic.update(source = tagdate.source)
                    tag_dic.update(le_status = tagdate.le_status)
                    tag_dic.update(motion = tagdate.motion)
                    tag_dic.update(solution = tagdate.solution)
                    tag_dic.update(x = tagdate.x)
                    tag_dic.update(y = tagdate.y)
                    tag_dic.update(z = tagdate.z)
                    m_tags_list.append(tag_dic)
                return m_tags_list
        data=dict()
        data.update(status=-100)
        data.update(error="system error : invalid parameters")
        return data
    except Exception as error:
        logging.error(str(traceback.format_exc()))
        data=dict()
        data.update(status=-100)
        data.update(error="system error : "+str(traceback.format_exc()))
        return data
 

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
    return "OK"


@csrf_exempt #Список Подразделений
def getListDepartments(user): #Список Подразделений
    departM = []
    alldepatment=Department.objects.filter().all()
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
    allposition=Position.objects.filter()
    for position in allposition:
        name=position.name
        p=dict()
        p.update(id=position.id)
        p.update(name=name)
        p.update(nameb=name.encode('cp1251').decode('cp1251'))
        positionM.append(p)    
    return positionM

@csrf_exempt #Список работников
def getListWorkers(user): #Список работников
    workerM = []
    worker_list=Worker.objects.order_by('name').all()
    for worker in worker_list:
        
        department = dict()
        if worker.department is not None:
            department.update(id = worker.department.id)
            department.update(name = worker.department.name)
        position = dict()
        if worker.position is not None:
            position.update(id = worker.position.id)
            position.update(name = worker.position.name)
        
        catalog = dict()
        catalog.update(tabnomer = worker.tabnomer)
        catalog.update(name = worker.name)
        catalog.update(lastName = worker.lastName)
        catalog.update(firstName = worker.firstName)
        catalog.update(otchestvo = worker.otchestvo)
        catalog.update(sex_workers = worker.sex_workers)
        catalog.update(position = position)
        catalog.update(department = department)
        catalog.update(uid = worker.uid)
        workerM.append(catalog)    
    return workerM


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

