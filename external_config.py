# candice configuration file
# name reflects audience, ie.
#
# internal_config.py is the internal proxy config
# external_config.py is the external
# repeater_config.py is the repeater, etc
#
# this can be changed by modifying each script
# if something special needs to be done

# host_drive
# The path to the proxy's storage/db directory
# Absolute path
# Internal/External/Repeater

host_drive = '/home/james/mirror'

# redirect_port
# Port used to handle incoming redirected connections
# Integer, used for redirect proxy (usually internal)
# Default: 3128
# Internal
#redirect_port = 3128

# redirect_web_host
# Server used to pass on connections to internal proxy
# Default: localhost
# Internal
#redirect_web_host = 'localhost'

# redirect_web_port
# Port used to pass on connections to internal proxy (requests, not content)
# Should be the same as used by web_server_port
# Default: 80
# Internal
#redirect_web_port = 80

# content_port
# Port used to serve cached content
# Default: 8080
# Internal
#content_port = 8080

# web_server_port
# Port used to host django and manage user requests
# Default: 80
# Internal
#web_server_port = 80

# web_server_interface
# Interface used to host internal connections
# Default: eth0 or eth1
# Internal
#web_server_interface = ''