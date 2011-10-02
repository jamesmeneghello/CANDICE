from candice_types import ProxyBase
from django.conf import settings

host_drive = '/home/james/tmpdev/repeater/'

class RepeaterProxy(ProxyBase):
    def __init__(self):
        ProxyBase.__init__(self)
        self.default_db = 'host'
    
    def begin(self):
        print('Are you (d)ropping data off, or (c)ollecting it?')
        self.task = raw_input()
        ProxyBase.begin(self)

    def process(self, request):
        if self.task == 'd':
            self.incoming(request)
            request.save(using='host')
            request.delete(using='courier')
        elif self.task == 'c':
            self.outgoing(request)
            request.save(using='courier')
            request.delete(using='host')

    def get_requests(self):
        from handle.models import Request
        if self.task == 'd':
            req = Request.objects.using('courier').all()
        elif self.task == 'c':
            req = Request.objects.using('host').all()

        self.requests = req

    def outgoing(self, request):
        ProxyBase.outgoing(self, request)
        request.host_store.flush()

settings.configure()
proxy = RepeaterProxy()
proxy.host_path = host_drive
print('Listening for usb devices...')
proxy.start()