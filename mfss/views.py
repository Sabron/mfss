from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from users.models import Profile

from apps.util import generalmodule 

def user_block(request,user):
    profile=Profile.objects.filter(user=user).first()
    if not profile:
        return False;
    if profile.block:
        return False
    return True

def user_api(request,user):
    profile=Profile.objects.filter(user=user).first()
    if not profile:
        return False;
    if profile.api_client:
        return True
    return False

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user_api(request,user):
                context={
                     'error' :True,
                     'comment':'API пользователь не имеет доступ к Личному Кабинету',
                     }
                return render(request, 'registration/login.html', context)

            if user_block(request,user):
                login(request, user)
                context={
                        'user' : user,
                        'login' :username,
                        'logout':'accounts/logout/',
                        }
                return HttpResponseRedirect('/', context)
            else:
                context={
                     'error' :True,
                     'login' :username,
                     'comment':'Пользователь заблокирован',
                     }
                return render(request, 'registration/login.html', context)
        else:
            context={
                     'error' :True,
                     'login' :username,
                      'comment':'Не верный логин или пароль',
                     }
            return render(request, 'registration/login.html', context)
    else:
        if request.user.is_anonymous :
            context={
                'error' :False,
                    'comment':'',
                    }
            return render(request, 'registration/login.html', context)

        else:
            return redirect("/")
 

def user_logout(request):
    logout(request)
    context={
           'user' : '',
           'logout':'accounts/logout/',
            }
    return HttpResponseRedirect('/', context)