import urlparse, sys, os
from urllib import quote as urlquote
from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.python import log
from candice_types import InternalProxy, ExternalProxy, HttpRequest, UrlStorage
from django.conf import settings
log.startLogging(sys.stdout)

host_drive = '/home/james/tmpdev/host/'

databases={
    'default':
    {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME':os.path.join(host_drive, 'CANDICE.db')
    },
}
whitehosts = ['127.0.0.1', 'localhost', '10.2.2.1']

class ProxyRequest(http.Request):
    def __init__(self, channel, queued, reactor=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor

    def process(self):
        headers = self.getAllHeaders().copy()
        if str(headers['host']) not in whitehosts:
            url = '/redirect/' + headers['host'] + self.uri
            self.content.seek(0,0)
            s = self.content.read()
            clientFactory = proxy.ProxyClientFactory(self.method, url, self.clientproto, headers, s, self)
            self.reactor.connectTCP('localhost', 80, clientFactory)
            print (url)
        else:
            print (headers['host'])
            url = self.uri
            self.content.seek(0,0)
            s = self.content.read()
            clientFactory = proxy.ProxyClientFactory(self.method, url, self.clientproto, headers, s, self)
            self.reactor.connectTCP(headers['host'], 80, clientFactory)

class TransparentProxy(http.HTTPChannel):
    requestFactory = ProxyRequest

class ProxyFactory(http.HTTPFactory):
    protocol = TransparentProxy

reactor.listenTCP(3128, ProxyFactory())
reactor.run()
