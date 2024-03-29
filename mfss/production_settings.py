import os
from PIL import Image
import numpy as np

DEBUG =True

TIME_ZONE = 'Asia/Krasnoyarsk'


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN",'1918979100:AAFfzejSMaK_MM_QEFqhqQbG1z7AN50Gexc')

# -----> CELERY
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
BROKER_URL = REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'
#CELERY_TASK_TRACK_STARTED = True
#CELERY_TASK_TIME_LIMIT = 30 * 60



ALLOWED_HOSTS = ['127.0.0.1','*',]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)
ATT_ROOT = '/home/mfss/mfss/static/att'
ADR_LOCAL ='carwash.hronos.su'
DOWNLOAD_ROOT = '/home/mfss/mfss/media/download'

DATABASES_NAME='mfss_db'


DATABASES = {
    'default': {
        'HOST': '192.168.10.2',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASES_NAME,
        'USER': 'mfss_user',
        'PASSWORD': 'Angstrem*45',
        'PORT': int(os.environ.get('POSTGRES_PORT', '5432')),
    },
    'mfsb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mfsb_agk',
        'USER': 'mfsb_agk',
        'PASSWORD': 'mfsb',
        'HOST': '192.168.10.2',
        'PORT': '5432',
    },
    'mfsb_skada': { # Системы контроля работы оборудования
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mfsb_skada',
        'USER': 'mfsb_skada',
        'PASSWORD': 'mfsb',
        'HOST': '192.168.10.2',
        'PORT': '5432',
    },
    'mfsb_ppz': { # Противопожарной защиты
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mfsb_ppz',
        'USER': 'mfsb_ppz',
        'PASSWORD': 'mfsb',
        'HOST': '192.168.10.2',
        'PORT': '5432',
    },
    'mfsb_skpv': { # Системы контроля пожарного водоснабжения
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mfsb_skpv',
        'USER': 'mfsb_skpv',
        'PASSWORD': 'mfsb',
        'HOST': '192.168.10.2',
        'PORT': '5432',
    },
    'mfsb_block': { # Блокировки
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mfsb_block',
        'USER': 'mfsb_block',
        'PASSWORD': 'mfsb',
        'HOST': '192.168.10.2',
        'PORT': '5432',
    },
    'ktp': { # Блокировки
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ktp',
        'USER': 'ktp_user',
        'PASSWORD': 'rb,thrjl',
        'HOST': '192.168.10.2',
        'PORT': '5432',
    },

}

img = Image.open(BASE_DIR+'/static/img//plan/inver/otm_102_zone.png')
x,y= img.size
MAS = np.eye(x, y)
for xx in range(0,x):
    for yy in range(0,y):
        p = img.getpixel((xx,yy))
        if p[1]!=0:
            MAS[xx][yy] = 1
        else:
            MAS[xx][yy] = 0
