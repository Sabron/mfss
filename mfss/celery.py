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
    'send-send_telegram_message-minute': {
        'task': 'apps.schedulers.tasks.update_ops_date',
        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
    'send-send_telegram_message-minute': {
        'task': 'apps.schedulers.tasks.update_ops_date10',
        'schedule': timedelta(seconds=10),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },

#    'send-send_telegram_message-minute': {
#        'task': 'tgbot.tasks.send_telegram_message',
#        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#    'schedulers-auto_checkin': {
#        'task': 'apps.schedulers.tasks.auto_checkin',
#        'schedule': crontab(minute=0, hour=19),  # 19:00 по Москве
#        #'schedule': crontab(minute='*/3'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#
#    'schedulers-auto_subscribe_payment': {
#        'task': 'apps.schedulers.tasks.update_subscribe_payment',
#        'schedule': crontab(minute=0, hour=18),  # 18:00 по Москве
#        #'schedule': crontab(minute='*/3'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },


}
    