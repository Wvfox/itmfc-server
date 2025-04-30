import os

import sys

sys.path.append('/var/www/apitest.itmfc.ru/')

sys.path.append('/var/www/apitest.itmfc.ru/venv/lib/python3.11/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django

django.setup()

from django.core.handlers import wsgi

application = wsgi.WSGIHandler()