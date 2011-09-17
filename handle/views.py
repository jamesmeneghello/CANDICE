# Create your views here.

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from models import Request
from candice.candice_types import URL, UrlStorage
from pprint import pprint
import os

image_media = ['jpg', 'png', 'gif', 'svg']
script_media = ['css', 'js']

index_file = 'index.html'

HOST_STORE = '/home/james/tmpdev/host'

def getifip(ifn):
    import socket, fcntl, struct
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', ifn[:15]))[20:24])

def Redirect(request, url):
    u = URL(url)
    u.inject_query(request.GET)
    print (u)
    return HttpResponseRedirect('http://%s/%s' % (getifip('eth1'), u.__str__().replace('http://', '')))

def RequestHandler(request, url):
    request_url = URL(url)
    robj = Request.objects.filter(target__contains=request_url.host)
    if robj:
        req = robj[0]
        req.url = request_url
        host_store = UrlStorage(req, HOST_STORE)
        data = {}
        if req.flag == 'completed':
            data = {'action_date':req.action_date}
        elif req.flag == 'requested':
            data = {'request_date':req.request_date}
        return RenderToolbar(req.url.__str__(), 'handle/toolbar_' + req.flag + '.inc', data)
    else:
        return RenderToolbar(request_url.__str__(), 'handle/toolbar_request.inc')

def RenderToolbar(url, template, data = {}):
    print(url)
    
    SERVER_PORT = '8080'
    t = loader.get_template(template)
    server_addr = 'http://' + getifip('eth1')
    r = URL(url)
    cd = {
        'url' : server_addr + '/request/' + r.with_www().replace('http://',''),
        'page': server_addr + ':' + SERVER_PORT + '/' + r.with_www().replace('http://', '')
    }
    cd.update(data)
    c = Context(cd)
    return HttpResponse(t.render(c))

def MissingPage(url):
    return HttpResponse('The page %s is not in our cache.' % url)

def TakeRequest(request, url):
    request_url = URL(url)
    robj = Request.objects.filter(target__contains=request_url.host)
    if not robj:
        r = Request(request_type='HttpRequest', storage_type='UrlStorage', 
                    action='mirror', target=request_url.host, flag='requested')
    else:
        r = robj[0]
        r.flag = 'requested'

    r.save()

    return HttpResponseRedirect('http://%s/%s' % (getifip('eth1'), request_url.with_www().replace('http://', '')))