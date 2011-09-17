from candice_types import InternalProxy, ExternalProxy, HttpRequest, UrlStorage
import os
from django.conf import settings
from itertools import chain

courier_drive = '/home/james/tmpdev/courier/'
host_drive = '/home/james/tmpdev/host/'

databases={
    'default':
    {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME':os.path.join(courier_drive, 'Courier.db')
    },
    'courier':
    {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME':os.path.join(courier_drive, 'Courier.db')
    },
    'host':
    {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME':os.path.join(host_drive, 'CANDICE.db')
    },
}

if not databases:
    raise Exception('No database settings defined in external proxy!')
settings.configure(DATABASES=databases)

from handle.models import Request
reqs = list(chain(Request.objects.using('host').all(), Request.objects.using('courier').all()))
proxy = InternalProxy(reqs, host_drive, courier_drive)
proxy.begin()