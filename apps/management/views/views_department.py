import traceback

from django.db.models import Q
from django.core import exceptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect

from apps.catalog.models.model_departments import Department 
from apps.catalog.forms.form_department import DepartmentForm

from sabron.util import logging
from apps.util import generalmodule



@login_required(login_url='/accounts/login/?next=/management/?catalog=department&cmd=list')
@never_cache
def department_list(request): # Список подразделений
    try:
        param=request.GET.dict()
        clients=Department.objects.order_by("name").all()
        paginator = Paginator(clients, 50)
        page_number = request.GET.get('page',1)
        page=paginator.get_page(page_number)
        num_pages=page.paginator.num_pages
        num_pages_krat = num_pages//30
        list_num = int(page_number)//30
        if list_num<int(page_number)/30:
            list_num=list_num+1
        page_list_end=(list_num*30)+1
        if page_list_end>num_pages:
            page_list_end=num_pages+1
        page_list_start=((list_num*30)-30)+1
        if page_list_start<1:
            page_list_start=1
        page_list=range(page_list_start,page_list_end)
        end_page_list=list_num*30
        start_page_list=(list_num*30)-29
        if page.has_previous():
            perv_url='page={}'.format(page.previous_page_number())
        else:
            perv_url=''
        if page.has_next():
            next_url='page={}'.format(page.next_page_number())
        else:
            next_url=''
        context = generalmodule.get_context_template()
        context.update({
                'page_object' : page,
                'is_paginated':page.has_other_pages(),
                'perv_url':perv_url,
                'next_url':next_url,
                'num_pages':num_pages,
                'menuopen':'menu-open',
                'puti':'Главная',
                'page_list':page_list,
                'end_page_list':end_page_list,
                'start_page_list':start_page_list,
                })
        return render(request,'department_list.html', context)
    except Exception as err:
        logging.error(traceback.format_exc())

@login_required(login_url='/accounts/login/?next=/management/?catalog=department&cmd=list')
@never_cache
def department_add(request):
    try:
        param=request.POST.dict()
        print(param)
        if request.method == "POST":
            form = DepartmentForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                department = form.save(commit=False)
                department.save()
                return redirect('/management/?catalog=department&cmd=list')
        else:
            form =DepartmentForm()
            context = generalmodule.get_context_template()
            context.update({
                'form':form,
                'mt':'add',
                 })
            return render(request, 'department_add.html',context)
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?catalog=department&cmd=list')


@login_required(login_url='/accounts/login/?next=/management/?catalog=department&cmd=list')
@never_cache
def department_edit(request): 
    try:
        param = request.POST.dict()
        department = Department.objects.get(id=param['id'])
        form = DepartmentForm(instance=department)
        return render(request, 'department_edit.html', {'form': form,'mt':'save','department':department})
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?catalog=department&cmd=list')

@login_required(login_url='/accounts/login/?next=/management/?catalog=department&cmd=list')
@never_cache
def department_save(request): 
    try:
        param = request.POST.dict()
        department = Department.objects.get(id=param['id'])
        form = DepartmentForm(request.POST,instance=department)
        if form.is_valid():
            department = form.save(commit=False)
            department.save()
        return redirect('/management/?catalog=department&cmd=list')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/?catalog=department&cmd=list')



@login_required(login_url='/')
@never_cache
def cmd_manager(request,get_parm):
    try:
        if get_parm['cmd']=='add':
            return department_add(request)
        if get_parm['cmd']=='list':
            return department_list(request)
        if get_parm['cmd']=='save':
            return department_save(request)
        if get_parm['cmd']=='edit':
            return department_edit(request)
        return redirect('/management?catalog=department&cmd=list')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management?catalog=department&cmd=list')


@login_required(login_url='/')
@never_cache
def main_index(request):
    try:
        if request.method == "GET":
            param=request.GET.dict()
            if 'cmd' in param:
                return cmd_manager(request,param)
        if request.method == "POST":
            param=request.GET.dict()
            if 'cmd' in param:
                return cmd_manager(request,param)
        return redirect('/management/')
    except Exception as err:
        logging.error(traceback.format_exc())
        return redirect('/management/')

