from twisted.python.filepath import FilePath
from twisted.web.static import File
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web import static, resource, server, wsgi, static
from twisted.internet import reactor  
from candice_types import InternalProxy, ExternalProxy, HttpRequest, UrlStorage, ProxyBase
import os
from django.conf import settings
from itertools import chain

host_drive = '/home/james/tmpdev/host/'

databases={
    'default':
    {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME':os.path.join(host_drive, 'CANDICE.db')
    },
}

class UrlServer(ProxyBase):
    def __init__(self, requests, host_path, courier_path):
        super(UrlServer, self).__init__(requests, host_path, courier_path)
        self.resource = resource.Resource()

    def begin(self):
        for request in self.requests:
            self.setup(request)
            last_base_path = request.host_store.get_base_path()
            #self.process(request)

        self.resource = static.File(last_base_path)
        self.resource.indexNames=['index.html', 'index.htm']

    def process(self, request):
        self.resource.putChild(request.url.with_www().replace('http://', ''), File(request.host_store.get_path()))

if not databases:
    raise Exception('No database settings defined in server!')
try:
    settings.configure(DATABASES=databases)
except RuntimeError as e:
    pass
from handle.models import Request

reqs = Request.objects.all()
us = UrlServer(reqs, host_drive, '')
us.begin()

http_factory = server.Site(us.resource, logPath="content.log")
reactor.listenTCP(8080, http_factory)
reactor.run()