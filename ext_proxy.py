from candice_types import ProxyBase
from django.conf import settings
import datetime

execfile('external_config.py')

class ExternalProxy(ProxyBase):
    def __init__(self):
        ProxyBase.__init__(self)
        self.default_db = 'host'
    
    def incoming(self, request):
        ProxyBase.incoming(self, request)

        try:
            func = getattr(request.request_handler, request.action)
        except AttributeError:
            print('Request called handler action that doesn\'t exist.')
            sys.exit()
        else:
            func()
            request.action_date = datetime.datetime.now()

    def process(self, request):
        if request.flag == 'retrieved':
            self.outgoing(request)
            request.save(using='courier')
            request.delete(using='host')
        elif request.flag == 'requested':
            self.incoming(request)
            if request.host_store.exists():
                request.flag = 'retrieved'
            else:
                request.flag = 'error'
            request.save(using='host')
            request.delete(using='courier')

settings.configure()
proxy = ExternalProxy()
proxy.host_path = host_drive
print('Listening for usb devices...')
proxy.start()