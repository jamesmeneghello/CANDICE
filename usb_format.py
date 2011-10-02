from django.conf import settings
import argparse, os, sys

parser = argparse.ArgumentParser(description='Format a folder for host or courier duties.')
parser.add_argument('path', help='Path to a device or folder to format.')
parser.add_argument('-t', '--type', choices=['host','courier'], help='Whether to format as a host or courier device', required=True, dest='type')

args = parser.parse_args()

apps = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'candice.handle',
    'django_extensions',
)
sys.path.append('/home/james/ict617')

if args.type == 'courier':
    print (os.path.join(args.path, 'Courier.db'))
    settings.configure(INSTALLED_APPS = apps, DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3', 'NAME':os.path.join(args.path, 'Courier.db')}})
elif args.type == 'host':
    settings.configure(INSTALLED_APPS = apps, DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3', 'NAME':os.path.join(args.path, 'CANDICE.db')}})

from django.core import management

try:
    management.call_command('syncdb')
except Exception as e:
    print(e)
    print('Try running as root?')
    sys.exit()

print('Format complete.')