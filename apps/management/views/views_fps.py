import traceback

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django import forms
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect

from apps.fps.forms.form_fps_sensor import FpsSensorForm
from apps.fps.models.model_sensor import FpsSensor
from apps.main.models.model_datamfsb_skada import DataMfsbSkada

from apps.catalog.models.model_zones import Zone

from sabron.util import logging
from apps.util import generalmodule


@login_required(login_url='/')
@never_cache
def add_fps(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            form = FpsSensorForm(request.POST)
            if form.is_valid():
                fps = form.save(commit=False)
                fps.save()
                return redirect('/management/?module=fps&t=param')
        else:
            sensor_list = FpsSensor.objects.values('name').order_by('tag').distinct()
            data_mfsb = DataMfsbSkada.objects.values('name').filter(~Q(name__in=sensor_list)).order_by('name').distinct()
            form =FpsSensorForm()
            form.fields['zone'] = forms.ModelChoiceField(queryset = Zone.objects.all(),widget=forms.Select(attrs={'class':'form-control select2'})) 
            context = generalmodule.get_context_template()
            context.update({
                'form':form,
                'mt':'add',
                'data_mfsb':data_mfsb,
                 })
            return render(request, 'fps_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=fps&t=param')

@login_required(login_url='/')
@never_cache
def edit_fps(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            sensor_list = FpsSensor.objects.values('name').order_by('tag').distinct()
            data_mfsb = DataMfsbSkada.objects.values('name').filter(~Q(name__in=sensor_list)).order_by('name').distinct()
            accs_sensor = FpsSensor.objects.get(id=param['id'])
            form = FpsSensorForm(instance=accs_sensor)
            form.fields['zone'] = forms.ModelChoiceField(queryset = Zone.objects.all(),widget=forms.Select(attrs={'class':'form-control select2'})) 
            context = generalmodule.get_context_template()
            context.update({
                'mt':'save',
                'form':form,
                'accs_sensor':accs_sensor,
                'data_mfsb':data_mfsb,
                 })
            return render(request, 'fps_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=fps&t=param')

@login_required(login_url='/')
@never_cache
def save_fps(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            accs_sensor = FpsSensor.objects.get(id=param['id'])
            form = FpsSensorForm(request.POST,instance=accs_sensor)
        if form.is_valid():
            accs_sensor = form.save(commit=False)
            accs_sensor.save()
        return open_type(request,request.GET.dict())
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=fps&t=param')

@login_required(login_url='/')
@never_cache
def open_type(request,get_parm):
    try:
        context = generalmodule.get_context_template()
        accs_sensor_list = FpsSensor.objects.all().order_by("zone").order_by("name")
        sensor_count_active = FpsSensor.objects.filter(active=True).all().count()
        sensor_count = accs_sensor_list.count()
        sensor_count_noactive = sensor_count - sensor_count_active;
        context.update({
            'accs_sensor_list':accs_sensor_list,
            'sensor_count':sensor_count,
            'sensor_count_active':sensor_count_active,
            'sensor_count_noactive':sensor_count_noactive
                 })
        return render(request, 'fps_settings.html', context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')



@login_required(login_url='/')
@never_cache
def cmd_manager(request,get_parm):
    try:
        if get_parm['cmd']=='add':
            return add_fps(request)
        if get_parm['cmd']=='save':
            return save_fps(request)
        if get_parm['cmd']=='edit':
            return edit_fps(request)
        return redirect('/management/module=fps&t=param')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=fps&t=param')


@login_required(login_url='/')
@never_cache
def main_index(request):
    try:
        if request.method == "GET":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='fps':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return fps_list(request)
        if request.method == "POST":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='fps':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return fps_list(request)
        return redirect('/management/')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')

