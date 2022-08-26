import os

DEBUG =False

TIME_ZONE = 'Europe/Moscow'


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN",'1886949342:AAHJtTvmhdKCu506XSZi5q0bpNRUtZSR53k')

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
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASES_NAME,
        'USER': 'mfss_user',
        'PASSWORD': 'Angstrem*45',
        'PORT': int(os.environ.get('POSTGRES_PORT', '5432')),
    },
    'mfsb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mfsb',
        'USER': 'mfsb_user',
        'PASSWORD': 'mfsb',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}
                                                    	
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'formatters': {
#       'console': {
#            'format': '%(name)-12s %(levelname)-8s %(message)s'
#        },
#        'file': {
#            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
#        }
#   },
#    'handlers': {
#       'console': {
#            'class': 'logging.StreamHandler',
#            'formatter': 'console'
#        },
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'formatter': 'file',
#            'filename': 'debug.log'
#        }
#    },
#    'loggers': {
#        '': {
#            'level': 'DEBUG',
#            'handlers': ['console', 'file']
#        }
#    }
#}