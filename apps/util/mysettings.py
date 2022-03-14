# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from apps.util import generalmodule
from users.models import Profile
from django.utils.html import conditional_escape, format_html

from apps.util import generalmodule


register = template.Library()


# Регистрируем тег, с помощью которого будем получать атрибуты из файла settings
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.simple_tag
def settings_client(user,name):
    pr=Profile.objects.filter(user=user).first()
    dictSettings=generalmodule.getSettingsClient(pr.client)
    if name=='infoblock':
        html="""
                <div id='infobox' class=' box  hronos-alert'>
                    <div class='box-header'>
                        <h3 class='box-title'>Внимание !</h3>
                        <div class='box-tools pull-right'>
                            <button type='button' class='btn btn-box-tool' data-widget='remove'><i class='fa fa-remove'></i></button>
                        </div>
                    </div>
                <div class='box-body'>
                    <h4 style='color:red;'>Ваша учетная запись будет заблокирована c """+dictSettings['ДатаБлокировкиКлиента']+""" </h4>
                </div>
                </div>       
            """
        if dictSettings['ДатаБлокировкиКлиента']=='':
            html=''
        return format_html(html)

    return ''
    #return getattr(settings, name, "")


 