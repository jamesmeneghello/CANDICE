import subprocess
import shutil, os, sys
import urlparse, glob, urllib
import tldextract
import distutils.dir_util

class URL(object):
    def __init__(self, url):
        self.url = url
        self.parse()
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def fixurl(self):
        if self.url.find('http://') == -1:
            self.url = 'http://' + self.url

    def fixuri(self):
        if self.uri.rpartition('.')[0] == '':
            if self.uri.rpartition('/')[2] != '':
                #self.uri = self.uri + '/'
                pass

    def with_www(self):
        if self.host.find('www') == -1:
            host = 'www.' + self.host
        else:
            host = self.host
        return urlparse.urlunsplit([self.proto, host, self.uri, self.query, self.fragment])

    def tld(self):
        return tldextract.extract(self.url)['domain']

    def parse(self):
        self.fixurl()
        parts = urlparse.urlparse(self.url)
        self.proto = parts[0]
        self.host = parts[1]
        self.uri = parts[2]
        self.query = parts[3]
        self.fragment = parts[4]
        self.fixuri()

    def inject_query(self, data):
        qs = '&'.join([k+'='+urllib.quote(str(v)) for (k,v) in data.items()])
        self.query = qs

    def __unicode__(self):
        return urlparse.urlunsplit([self.proto, self.host, self.uri, self.query, self.fragment])

######################################################

class ProxyBase(object):
    def __init__(self, requests, host_path, courier_path):
        self.requests = requests
        self.host_path = host_path
        self.courier_path = courier_path

    def begin(self):
        for request in self.requests:
            self.setup(request)
            self.process(request)
            self.finalise(request)

    def setup(self, request):
            request.request_handler = request_types[request.request_type](request)
            request.host_store = storage_types[request.storage_type](request, self.host_path)
            request.courier_store = storage_types[request.storage_type](request, self.courier_path)

    def process(self, request):
        raise NotImplementedError('No proxy process code!')

    def finalise(self, request):
        raise NotImplementedError('No proxy finalise code!')

############

class ExternalProxy(ProxyBase):
    def __init__(self, requests, host_path, courier_path):
        super(ExternalProxy, self).__init__(requests, host_path, courier_path)

    def process(self, request):
        print('Processing proxy...')
        request.request_handler.external_action()

    def finalise(self, request):
        print('Finalising request...')
        request.request_handler.post_external()

############

class InternalProxy(ProxyBase):
    def __init__(self, requests, host_path, courier_path):
        super(InternalProxy, self).__init__(requests, host_path, courier_path)

    def process(self, request):
        print('Processing proxy...')
        request.request_handler.internal_action()

    def finalise(self, request):
        print('Finalising request...')
        request.request_handler.post_internal()

######################################################

class StorageBase(object):
    def __init__(self, request, storage_path):
        self.request = request
        self.storage_path = storage_path

    def store(self, src_dir):
        raise NotImplementedError('No function to store!')

    def flush(self):
        raise NotImplementedError('No function to flush!')

    def get_path(self):
        raise NotImplementedError('No get_dir function!')

    def get_base_path(self):
        return self.storage_path

##################

class UrlStorage(StorageBase):
    def store(self, data):
        if data:
            print('Storing data...')
            distutils.dir_util.copy_tree(data, self.get_path())
    
    def flush(self):
        print('Removing data...')
        distutils.dir_util.remove_tree(self.get_path())

    def get_path(self):
        return os.path.join(self.storage_path, 'data', self.request.url.with_www().replace('http://',''))

    def get_base_path(self):
        return os.path.join(self.storage_path, 'data')

######################################################

class RequestBase(object):
    def __init__(self, request):
        self.request = request

    def internal_action(self):
        raise NotImplementedError('No internal action!')

    def external_action(self):
        raise NotImplementedError('No external action!')

    def post_internal(self):
        pass
    
    def post_external(self):
        pass

##################

class HttpRequest(RequestBase):
    def __init__(self, request):
        super(HttpRequest, self).__init__(request)
        self.request.url = URL(request.target)

    def internal_action(self):
        print('Executing internal action')
        if self.request.flag == 'retrieved':
            self.request.host_store.store(self.request.courier_store.get_path())
            self.request.courier_store.flush()
            self.request.flag = 'completed'
        elif self.request.flag == 'error':
            pass
        elif self.request.flag == 'requested':
            pass

    def external_action(self):
        print('Executing external action...')
        if self.request.flag == 'requested':
            if self.request.action == 'mirror':
                self.mirror()
        
            if os.path.exists(self.request.host_store.get_path()):
                self.request.courier_store.store(self.request.host_store.get_path())
                self.request.flag = 'retrieved'
            else:
                self.request.flag = 'error'

    def post_internal(self):
        if self.request.flag == 'completed':
            self.request.save(using='host')
            self.request.delete(using='courier')
        elif self.request.flag == 'requested':
            self.request.save(using='courier')
            self.request.flag = 'transit'
            self.request.save(using='host')

    def post_external(self):
        self.request.save(using='courier')

    def mirror(self):
        print('Beginning mirror...')

        args = ['wget', '-e', 'robots=off', '-N', '-nv', 
                '-r', '-l', '3', '-p', '-t', '3', '-T', 
                '10', '-4', '-k', '-U', 
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535', 
                '--no-cookies', '--ignore-length', '--no-check-certificate', 
                '--no-remove-listing', '--html-extension', 
                '-P', self.request.host_store.get_base_path(), self.request.url.with_www()]
            
        retcode = subprocess.call(args)

######################################################

request_types = {
    'HttpRequest': HttpRequest
}

storage_types = {
    'UrlStorage': UrlStorage
}
