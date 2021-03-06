
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = False

"""
    Если True При каждом запуске браузера будет
    требовать авторизацию 'используются временные куки'
    """
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'sabron.apps.SabronConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'apps.adm_sys.apps.adm_sysConfig',

    #'api.v1.apps.Apiv1Config',
    #'apps.catalog.apps.CatalogConfig',
    #'apps.documents.apps.DocumentsConfig',
    'apps.main.apps.MainConfig',
    'apps.acs.apps.acsConfig',
    
]

"""Информация о приложении """
SITE_TITLE = u'Многофункциональная система безопасности'
SITE_TITLE_S = u'МФСБ'
APP_VER = u'1.0.00.2'
APP_COPPIRIGHT = u'Многофункциональная система безопасности'


KEYWORDS = u''
DESCRIPTION = u"Многофункциональная система безопасности"
AUTHOR = u'Киберкод'
