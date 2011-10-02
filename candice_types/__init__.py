import subprocess
import shutil, os, sys
import urlparse, glob, urllib
import distutils.dir_util
import dbus, gobject
import datetime
from itertools import chain
from dbus.mainloop.glib import DBusGMainLoop
from django.conf import settings
#from candice_types.request import request_types
#from candice_types.storage import storage_types

class URL():
    def __init__(self, url):
        self.url = url
        
        # add http if it doesn't exist
        self.fixurl()

        # auto-parse the url, because we're unlikely to ever not want it parsed
        self.parse()
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def fixurl(self):
        # irritatingly, urlparse treats urls not starting with a protocol
        # as relative paths, so we add it manually
        if self.url.find('http://') == -1:
            self.url = 'http://' + self.url

    def fixuri(self):
        if self.uri.rpartition('.')[0] == '':
            if self.uri.rpartition('/')[2] != '':
                #self.uri = self.uri + '/'
                pass

    def with_www(self):
        # manually add a www, as some sites require it and others don't,
        # but it's safer to force it. however, this means some sites
        # don't get hit properly - lack of config standards strikes again
        if self.host.find('www') == -1:
            host = 'www.' + self.host
        else:
            host = self.host

        # rebuild the url and return it without mutating this object
        return urlparse.urlunsplit([self.proto, host, self.uri, self.query, self.fragment])

    
    # no longer necessary but might be useful in the future
    #def tld(self):
    #    return tldextract.extract(self.url)['domain']
        
    def parse(self):
        # split it into component parts
        parts = urlparse.urlparse(self.url)
        self.proto = parts[0]
        self.host = parts[1]
        self.uri = parts[2]
        self.query = parts[3]
        self.fragment = parts[4]
        self.fixuri()

    def inject_query(self, data):
        # join querystring vars together
        qs = '&'.join([k+'='+urllib.quote(str(v)) for (k,v) in data.items()])
        self.query = qs

    def __unicode__(self):
        # crush it back into a url
        return urlparse.urlunsplit([self.proto, self.host, self.uri, self.query, self.fragment])

######################################################

class ProxyBase():
    def __init__(self):
        self.requests = []
        self.courier_path = ''
        self.host_path = ''
        self.databases = {}
        self.default_db = ''
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()

    def device_added(self, device):
        # build udisk connection for this device
        dev_obj = self.bus.get_object('org.freedesktop.UDisks', device)
        dev_props = dbus.Interface(dev_obj, dbus.PROPERTIES_IFACE)
        
        # grab the mount point of the inserted device
        courier_path = dev_props.Get('org.freedesktop.UDisks.Device', 'DeviceMountPaths')

        for path in courier_path:
            print ('Device: ' + path)
            # if the drive is "formatted" as a courier disk
            if os.path.exists(os.path.join(path, 'Courier.db')):
                print('Compatible device found!')

                # we found a courier, so set the path and start the setup
                self.courier_path = path
                self.begin()

    def database(self):
        engine = 'django.db.backends.sqlite3'
        
        # if there's a courier drive inserted
        if self.courier_path:
            # set up the database and add it to the db config
            courier_database = {
                'ENGINE':engine,
                'NAME':os.path.join(self.courier_path, 'Courier.db')
            }
            self.databases.update({'courier':courier_database})

        # same deal for a host drive
        if self.host_path:
            host_database = {
                'ENGINE':engine,
                'NAME':os.path.join(self.host_path, 'CANDICE.db')
            }
            self.databases.update({'host':host_database})
        
        # if the proxy's constructor hasn't set which default db to use,
        # sperg out
        if not self.default_db:
            print('Missing default database parameter in proxy!')
            sys.exit()
        
        # leave it up to the implementation to choose a default
        self.databases.update({'default':self.databases[self.default_db].copy()})
        
        # update django db conf forcefully (the devs would hate this :D)
        settings.DATABASES = self.databases

    def start(self):
        # set up overall dbus connection
        proxy = self.bus.get_object('org.freedesktop.UDisks', '/org/freedesktop/UDisks')
        iface = dbus.Interface(proxy, 'org.freedesktop.UDisks')

        # register callback on device_added
        iface.connect_to_signal('DeviceAdded', self.device_added)

        # start the dbus checking loop
        mainloop = gobject.MainLoop()
        mainloop.run()

    def get_requests(self):
        from handle.models import Request
        c_req = []
        h_req = []
        if self.courier_path:
            c_req = Request.objects.using('courier').all()
        if self.host_path:
            h_req = Request.objects.using('host').all()

        # join either/both host and courier into a single list
        self.requests = list(chain(c_req, h_req))

    def begin(self):
        self.database()
        self.get_requests()
        for request in self.requests:
            print('Processing request %s...' % request)
            self.setup(request)
            self.process(request)
            print('Request completed.')
        print('Completed for now, moving back to wait mode...')

    def setup(self, request):
            request.request_handler = request_types[request.request_type](self, request)
            request.host_store = storage_types[request.storage_type](request, self.host_path)
            request.courier_store = storage_types[request.storage_type](request, self.courier_path)

    def process(self, request):
        raise NotImplementedError('No proxy process code!')

    def incoming(self, request):
        if request.courier_store.exists():
            request.host_store.store(request.courier_store.get_path())
            request.courier_store.flush()
        
    def outgoing(self, request):
        if request.host_store.exists():
            request.courier_store.store(request.host_store.get_path())

############

class StorageBase():
    def __init__(self, request, storage_path):
        self.request = request
        self.storage_path = storage_path

    def store(self, src):
        raise NotImplementedError('No function to store!')

    def flush(self):
        raise NotImplementedError('No function to flush!')

    def get_path(self):
        raise NotImplementedError('No get_dir function!')

    def get_base_path(self):
        return self.storage_path

    def exists(self):
        raise NotImplementedError('No exists function!')

##################

class RequestBase():
    def __init__(self, proxy, request):
        self.proxy = proxy
        self.request = request

##################
