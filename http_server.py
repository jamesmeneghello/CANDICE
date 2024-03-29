from twisted.web import static, resource, server, wsgi, static
from twisted.python import threadpool
from twisted.application import internet, service
from twisted.internet import reactor
import os, sys

execfile('internal_config.py')

# set up django environment variables
sys.path.append('/home/james/ict617/candice')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.handlers.wsgi import WSGIHandler

class RootResource(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    return wsgi.WSGIResource(reactor, pool, WSGIHandler())

def get_root_resource():
    wsgi_root = wsgi_resource()
    return RootResource(wsgi_root)

#Twisted Application setup:
application = service.Application('candice')
serviceCollection = service.IServiceCollection(application)

# Django and static file server:
root_resource = get_root_resource()
root_resource.putChild("static", static.File("static"))
http_factory = server.Site(root_resource)
internet.TCPServer(web_server_port, http_factory).setServiceParent(serviceCollection)