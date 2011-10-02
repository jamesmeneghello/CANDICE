from candice_types import RequestBase

class HttpRequest(RequestBase):
    def __init__(self, proxy, request):
        RequestBase.__init__(self, proxy, request)
        self.request.url = URL(request.target)

    def mirror(self):
        print('Beginning mirror...')

        args = ['wget', '-e', 'robots=off', '-N', '-nv', 
                '-r', '-l', '3', '-p', '-t', '3', '-T', 
                '10', '-4', '-k', '-U', 
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535', 
                '--no-cookies', '--ignore-length', '--no-check-certificate', 
                '--no-remove-listing', '--html-extension', '--restrict-file-names=windows',
                '-P', self.request.host_store.get_base_path(), self.request.url.with_www()]
            
        retcode = subprocess.call(args)

request_types = {
    'HttpRequest': HttpRequest
}
