
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = False

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
    'apps.ops.apps.OpsConfig',
    'django_celery_beat', 

    'apps.catalog.apps.CatalogConfig',		
    'apps.schedulers.apps.SchedulersConfig',
    'apps.main.apps.MainConfig',
    'apps.acs.apps.acsConfig',
    'apps.eps.apps.epsConfig',
]

"""Информация о приложении """
SITE_TITLE = u'Многофункциональная система безопасности'
SITE_TITLE_S = u'МФСБ'
APP_VER = u'1.0.01.9'
APP_COPPIRIGHT = u'Многофункциональная система безопасности'


KEYWORDS = u''
DESCRIPTION = u"Многофункциональная система безопасности"
AUTHOR = u'Киберкод'
