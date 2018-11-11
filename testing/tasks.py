from __future__ import absolute_import, unicode_literals

import digitalocean
from decouple import config

from codelnmain.celery import app

DO_TOKEN = config('DO_TOKEN')
api_base = 'https://api.digitalocean.com/v2'


@app.task
def digital_ocean(project_id):
    # project = get_object_or_404(Project, id=project_id)
    droplet = digitalocean.Droplet(token=DO_TOKEN, name='charlestrial', image='40141728', region='ams3',
                                   size_slug='4gb', size='')
    droplet.create()
    # get_droplet_status(droplet.id, project_id)
    return droplet.id


@app.task
def get_droplet_status(droplet_id, project_id):
    manager = digitalocean.Manager(token=DO_TOKEN)
    droplet = manager.get_droplet(id)
    if droplet.status == 'active':
        pass
    else:
        get_droplet_status.delay(droplet_id, project_id, countdown=60)
