import traceback

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django import forms
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect

from apps.scada.forms.form_scada_sensor import ScadaSensorForm
from apps.scada.models.model_sensor import ScadaSensor
from apps.acs.models.model_indicators import AcsIndicators
from apps.main.models.model_datamfsb_skada import DataMfsbSkada

from apps.catalog.models.model_zones import Zone

from sabron.util import logging
from apps.util import generalmodule


@login_required(login_url='/')
@never_cache
def edit_scada(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            sensor_list = ScadaSensor.objects.values('name').order_by('tag').distinct()
            accs_sensor = ScadaSensor.objects.get(id=param['id'])
            form = ScadaSensorForm(instance=accs_sensor)
            form.fields['zone'] = forms.ModelChoiceField(queryset = Zone.objects.all(),widget=forms.Select(attrs={'class':'form-control select2'})) 
            form.fields['zone'].required = False
            context = generalmodule.get_context_template()
            context.update({
                'mt':'save',
                'form':form,
                'accs_sensor':accs_sensor,
                 })
            return render(request, 'scada_sensor_edit.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=scada&t=param')

@login_required(login_url='/')
@never_cache
def save_scada(request):
    try:
        param=request.POST.dict()
        if request.method == "POST":
            accs_sensor = ScadaSensor.objects.get(id=param['id'])
            form = ScadaSensorForm(request.POST,instance=accs_sensor)
        if form.is_valid():
            accs_sensor = form.save(commit=False)
            accs_sensor.save()
        return open_type(request,request.GET.dict())
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=scada&t=param')

@login_required(login_url='/')
@never_cache
def open_type(request,get_parm):
    try:
        context = generalmodule.get_context_template()
        accs_sensor_list = ScadaSensor.objects.all().order_by("zone").order_by("active")
        sensor_count_active = ScadaSensor.objects.filter(active=True).all().count()
        sensor_count = accs_sensor_list.count()
        sensor_count_noactive = sensor_count - sensor_count_active;
        context.update({
            'accs_sensor_list':accs_sensor_list,
            'sensor_count':sensor_count,
            'sensor_count_active':sensor_count_active,
            'sensor_count_noactive':sensor_count_noactive
                 })
        return render(request, 'scada_settings.html', context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')



@login_required(login_url='/')
@never_cache
def cmd_manager(request,get_parm):
    try:
        if get_parm['cmd']=='save':
            return save_scada(request)
        if get_parm['cmd']=='edit':
            return edit_scada(request)
        return redirect('/management/module=scada&t=param')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?module=scada&t=param')


@login_required(login_url='/')
@never_cache
def main_index(request):
    try:
        if request.method == "GET":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='scada':
                    if 'cmd' in param:
                        return cmd_manager(request,param)
                    elif 't' in param:
                        return open_type(request,param)
                    #else:
                    #    return acs_list(request)
        if request.method == "POST":
            param=request.GET.dict()
            if 'module' in param:
                if param['module']=='scada':
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


