from candice_types import ExternalProxy, HttpRequest, UrlStorage
import os
from django.conf import settings

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
}

if not databases:
    raise Exception('No database settings defined in external proxy!')
settings.configure(DATABASES=databases)

from handle.models import Request
reqs = Request.objects.all()
proxy = ExternalProxy(reqs, '/home/james/mirror/', courier_drive)
proxy.begin()