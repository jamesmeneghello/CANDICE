from candice_types import ProxyBase
from django.conf import settings

host_drive = '/home/james/tmpdev/host/'

class InternalProxy(ProxyBase):
    def __init__(self):
        ProxyBase.__init__(self)
        self.default_db = 'host'

    def process(self, request):
        if request.flag == 'requested':
            self.outgoing(request)
            request.save(using='courier')
            request.flag = 'transit'
            request.save(using='host')
        elif request.flag == 'retrieved':
            self.incoming(request)
            request.flag = 'completed'
            request.save(using='host')
            request.delete(using='courier')

settings.configure()
proxy = InternalProxy()
proxy.host_path = host_drive
print('Listening for usb devices...')
proxy.start()