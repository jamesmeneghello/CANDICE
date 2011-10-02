from twisted.python.filepath import FilePath
from twisted.web.static import File
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web import static, resource, server, wsgi, static
from twisted.internet import reactor  
import os


execfile('internal_config.py')

resource = resource.Resource()
resource = static.File(os.path.join(host_drive, 'data'))
resource.indexNames=['index.html', 'index.htm']

http_factory = server.Site(resource, logPath='content.log')
reactor.listenTCP(content_port, http_factory)
reactor.run()