from __future__ import absolute_import, unicode_literals
import digitalocean
from decouple import config
from codelnmain.celery import app
DO_TOKEN = config('DO_TOKEN')
api_base = 'https://api.digitalocean.com/v2'
@app.task
def digital_ocean(id):
    droplet = digitalocean.Droplet(token=DO_TOKEN, name='philtrial', image='ubuntu-16-04-x64', region='ams3', size_slug='1gb', size='')
    droplet.create()

@app.task
def assign_floating_ip(id):
   manager = digitalocean.Manager(token=DO_TOKEN)
   droplet = manager.get_droplet(id)
   floating_ip = '206.189.241.12'

@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
