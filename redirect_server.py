import urlparse, sys, os
from urllib import quote as urlquote
from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.python import log
log.startLogging(sys.stdout)

execfile('internal_config.py')

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
            self.reactor.connectTCP(redirect_web_host, redirect_web_port, clientFactory)
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

reactor.listenTCP(redirect_port, ProxyFactory())
reactor.run()
