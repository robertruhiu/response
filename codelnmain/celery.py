from __future__ import  absolute_import, unicode_literals
import os
from  decouple import config
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codelnmain.settings')

app = Celery('codelnmain', broker=config('REDIS_URL', default='redis://'),
             backend=config('REDIS_BACKEND', default='redis://'),)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_ACCEPT_CONTENT = ['application/json', 'pickle']
CELERY_TASK_SERIALIZER = 'pickle'
BROKER_URL = config('REDIS_URL', default='redis://')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://')
CELERY_RESULT_SERIALIZER = 'json'
