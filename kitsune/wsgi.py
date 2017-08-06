import os
import site
from datetime import datetime

try:
    import newrelic.agent
except ImportError:
    newrelic = False


if newrelic:
    newrelic_ini = os.getenv('NEWRELIC_PYTHON_INI_FILE', False)
    if newrelic_ini:
        newrelic.agent.initialize(newrelic_ini)
    else:
        newrelic = False


# Remember when mod_wsgi loaded this file so we can track it in nagios.
wsgi_loaded = datetime.now()

# Add kitsune to the python path
wsgidir = os.path.dirname(__file__)
site.addsitedir(os.path.abspath(os.path.join(wsgidir, '../')))

# For django-celery
os.environ['CELERY_LOADER'] = 'django'

# Import for side-effects: set-up
import manage

import django.conf
# import django.core.management
# import django.utils

# Do validate and activate translations like using `./manage.py runserver`.
# http://blog.dscpl.com.au/2010/03/improved-wsgi-script-for-use-with.html
# django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)
# utility = django.core.management.ManagementUtility()
# command = utility.fetch_command('runserver')
# command.validate()

# This is what mod_wsgi runs.
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
django_app = get_wsgi_application()

application = DjangoWhiteNoise(django_app)


# Uncomment this to figure out what's going on with the mod_wsgi environment.
# def application(env, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     return '\n'.join('%r: %r' % item for item in sorted(env.items()))

# vim: ft=python
