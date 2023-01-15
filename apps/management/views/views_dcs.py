import traceback

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect

from apps.dcs.forms.form_dsc_sensor import DcsSensorForm
from apps.dcs.models.model_sensor import DcsSensor
from apps.dcs.models.model_indicators import DcsIndicators
from apps.main.models.model_datamfsb import DataMfsb

from sabron.util import logging
from apps.util import generalmodule


@login_required(login_url='/')
@never_cache
def add_dcs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            form = DcsSensorForm(request.POST)
            if form.is_valid():
                dcs = form.save(commit=False)
                dcs.save()
                return redirect('/management/?module=dcs&t=param')
        else:
            sensor_list = DcsSensor.objects.values('name').order_by('tag').distinct()
            data_mfsb = DataMfsb.objects.values('name').filter(~Q(name__in=sensor_list)).order_by('name').distinct()
            form =DcsSensorForm()
            context = generalmodule.get_context_template()
            context.update({
                'form':form,
                'mt':'add',
                'data_mfsb':data_mfsb,
                 })
            return render(request, 'dcs_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=dcs&t=param')

@login_required(login_url='/')
@never_cache
def delete_dcs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            dcs_sensor = DcsSensor.objects.get(id=param['id'])
            DcsIndicators.objects.filter(sensor = dcs_sensor).delete()
            dcs_sensor.delete()
            return generalmodule.ReturnJson(200,data)
    except Exception as err:
        logging.error(traceback.format_exc())
        data=dict()
        data.update(status=-1)
        return generalmodule.ReturnJson(200,data)

@login_required(login_url='/')
@never_cache
def edit_dcs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            sensor_list = DcsSensor.objects.values('name').order_by('tag').distinct()
            data_mfsb = DataMfsb.objects.values('name').filter(~Q(name__in=sensor_list)).order_by('name').distinct()
            accs_sensor = DcsSensor.objects.get(id=param['id'])
            form = DcsSensorForm(instance=accs_sensor)
            context = generalmodule.get_context_template()
            context.update({
                'mt':'save',
                'form':form,
                'accs_sensor':accs_sensor,
                'data_mfsb':data_mfsb,
                 })
            return render(request, 'dcs_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=dcs&t=param')

@login_required(login_url='/')
@never_cache
def save_dcs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            accs_sensor = DcsSensor.objects.get(id=param['id'])
            form = DcsSensorForm(request.POST,instance=accs_sensor)
        if form.is_valid():
            accs_sensor = form.save(commit=False)
            accs_sensor.save()
        return open_type(request,request.GET.dict())
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=dcs&t=param')

@login_required(login_url='/')
@never_cache
def open_type(request,get_parm):
    try:
        context = generalmodule.get_context_template()
        accs_sensor_list = DcsSensor.objects.all().order_by("name")
        sensor_count_active = DcsSensor.objects.filter(active=True).all().count()
        sensor_count = accs_sensor_list.count()
        sensor_count_noactive = sensor_count - sensor_count_active;
        context.update({
            'accs_sensor_list':accs_sensor_list,
            'sensor_count':sensor_count,
            'sensor_count_active':sensor_count_active,
            'sensor_count_noactive':sensor_count_noactive
                 })
        return render(request, 'dcs_settings.html', context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')



@login_required(login_url='/')
@never_cache
def cmd_manager(request,get_parm):
    try:
        if get_parm['cmd']=='add':
            return add_dcs(request)
        if get_parm['cmd']=='save':
            return save_dcs(request)
        if get_parm['cmd']=='edit':
            return edit_dcs(request)
        if get_parm['cmd']=='delete':
            return delete_dcs(request)
        return redirect('/management/module=dcs&t=param')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=dcs&t=param')


@login_required(login_url='/')
@never_cache
def main_index(request):
    try:
        if request.method == "GET":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='dcs':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return dcs_list(request)
        if request.method == "POST":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='dcs':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return dcs_list(request)
        return redirect('/management/')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')

