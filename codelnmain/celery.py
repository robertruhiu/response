from __future__ import  absolute_import, unicode_literals
import os
from  decouple import config
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codelnmain.settings')


app = Celery()

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Africa/Accra',
    enable_utc=True,

)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

if __name__ == '__main__':
    app.start()