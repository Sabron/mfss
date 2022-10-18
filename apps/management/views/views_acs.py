import traceback

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect

from apps.acs.forms.form_asc_sensor import AcsSensorForm
from apps.acs.models.model_sensor import AcsSensor
from apps.main.models.model_datamfsb import DataMfsb

from sabron.util import logging
from apps.util import generalmodule


@login_required(login_url='/')
@never_cache
def add_acs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            form = AcsSensorForm(request.POST)
            if form.is_valid():
                acs = form.save(commit=False)
                acs.save()
                return redirect('/management/?module=acs&t=param')
        else:
            sensor_list = AcsSensor.objects.values('name').order_by('tag').distinct()
            data_mfsb = DataMfsb.objects.values('name').filter(~Q(name__in=sensor_list)).order_by('name').distinct()
            form =AcsSensorForm()
            context = generalmodule.get_context_template()
            context.update({
                'form':form,
                'mt':'add',
                'data_mfsb':data_mfsb,
                 })
            return render(request, 'acs_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=acs&t=param')

@login_required(login_url='/')
@never_cache
def edit_acs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            sensor_list = AcsSensor.objects.values('name').order_by('tag').distinct()
            data_mfsb = DataMfsb.objects.values('name').filter(~Q(name__in=sensor_list)).order_by('name').distinct()
            accs_sensor = AcsSensor.objects.get(id=param['id'])
            form = AcsSensorForm(instance=accs_sensor)
            context = generalmodule.get_context_template()
            context.update({
                'mt':'save',
                'form':form,
                'accs_sensor':accs_sensor,
                'data_mfsb':data_mfsb,
                 })
            return render(request, 'acs_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=acs&t=param')

@login_required(login_url='/')
@never_cache
def save_acs(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            accs_sensor = AcsSensor.objects.get(id=param['id'])
            form = AcsSensorForm(request.POST,instance=accs_sensor)
        if form.is_valid():
            accs_sensor = form.save(commit=False)
            accs_sensor.save()
        return open_type(request,request.GET.dict())
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=acs&t=param')

@login_required(login_url='/')
@never_cache
def open_type(request,get_parm):
    try:
        context = generalmodule.get_context_template()
        accs_sensor_list = AcsSensor.objects.all().order_by("name")
        sensor_count_active = AcsSensor.objects.filter(active=True).all().count()
        sensor_count = accs_sensor_list.count()
        sensor_count_noactive = sensor_count - sensor_count_active;
        context.update({
            'accs_sensor_list':accs_sensor_list,
            'sensor_count':sensor_count,
            'sensor_count_active':sensor_count_active,
            'sensor_count_noactive':sensor_count_noactive
                 })
        return render(request, 'acs_settings.html', context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')



@login_required(login_url='/')
@never_cache
def cmd_manager(request,get_parm):
    try:
        if get_parm['cmd']=='add':
            return add_acs(request)
        if get_parm['cmd']=='save':
            return save_acs(request)
        if get_parm['cmd']=='edit':
            return edit_acs(request)
        return redirect('/management/module=acs&t=param')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=acs&t=param')


@login_required(login_url='/')
@never_cache
def main_index(request):
    try:
        if request.method == "GET":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='acs':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return acs_list(request)
        if request.method == "POST":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='acs':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return acs_list(request)
        return redirect('/management/')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')

