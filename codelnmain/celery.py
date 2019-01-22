from __future__ import  absolute_import, unicode_literals
import os
from  decouple import config
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codelnmain.settings')


app = Celery('codelnmain',broker='amqp://ndjdevhx:r5qC0_UAj5gpxdXTZQxT-T46cjFcaihM@raven.rmq.cloudamqp.com/ndjdevhx',
             backend='redis://h:p5a5c90f64f97e2a76bdb9d86a7697143c1d835dd0d5103a48db8614d0c7d2611@ec2-52-16-97-46.eu-west-1.compute.amazonaws.com:10739',
             include=['frontend.tasks'])

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