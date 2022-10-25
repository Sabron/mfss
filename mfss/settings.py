import os
from sabron.util import logging

# -*- coding: utf-8 -*-
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '915ce6bb-13e2-486e-ad56-68ed68ef79c3'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_ROOT=os.path.join(BASE_DIR,'templates')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',       # РЈРїСЂР°РІР»РµРЅРёРµ СЃРµСЃСЃРёСЏРјРё РјРµР¶РґСѓ Р·Р°РїСЂРѕСЃР°РјРё
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',    # РЎРІСЏР·С‹РІР°РµС‚ РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№, РёСЃРїРѕР»СЊР·СѓСЋС‰РёС… СЃРµСЃСЃРёРё, Р·Р°РїСЂРѕСЃР°РјРё.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'mfss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_ROOT,'apps/main/templates',
                    'apps/management/templates',
                    'apps/eps/templates',
                    ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                      'mysettings': 'apps.util.mysettings',

            }
        },
    },
]


WSGI_APPLICATION = 'mfss.wsgi.application'
ASGI_APPLICATION = 'mfss.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


DOWNLOAD_URL = '/download/'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'

logging.set()


from .app_settings import *

try:
    from .local_settings import *
except ImportError:
    from .production_settings import *



