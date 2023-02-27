import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mfss.settings')

app = Celery('mfss')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.enable_utc = False
app.conf.beat_schedule = {
#    'send-send_telegram_message-minute': {
#        'task': 'apps.schedulers.tasks.update_ops_date',
#        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },



#    'apps.schedulers.tasks.update_ops_date': {# Получение данных АГК и КЗ
#        'task': 'apps.schedulers.tasks.update_ops_date',
#        'schedule': timedelta(seconds=10),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#    'apps.schedulers.tasks.update_ops_skpv_date': { # Получение данных со водоснабжение
#        'task': 'apps.schedulers.tasks.update_ops_skpv_date',
#        'schedule': timedelta(seconds=10),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#    'apps.schedulers.tasks.update_ops_ppz_date': { # Получение данных противопожарная защита
#        'task': 'apps.schedulers.tasks.update_ops_ppz_date',
#        'schedule': timedelta(seconds=10),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#  'apps.schedulers.tasks.update_ops_scada_date': { # Получение данных Системы контроля работы оборудования
#        'task': 'apps.schedulers.tasks.update_ops_scada_date',
#        'schedule': timedelta(seconds=10),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },

#    'apps.schedulers.tasks.update_eps': {
#        'task': 'apps.schedulers.tasks.update_eps',
#        'schedule': timedelta(minutes=5),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },



#    'send-send_telegram_message-minute': {
#        'task': 'tgbot.tasks.send_telegram_message',
#        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
    'schedulers-auto_delete': {
        'task': 'apps.schedulers.tasks.auto_ops_delete',
        'schedule': crontab(minute=0, hour=1),  # 01:00 по Москве
        #'schedule': crontab(minute='*/3'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
#
#    'schedulers-auto_subscribe_payment': {
#        'task': 'apps.schedulers.tasks.update_subscribe_payment',
#        'schedule': crontab(minute=0, hour=18),  # 18:00 по Москве
#        #'schedule': crontab(minute='*/3'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },


}
    