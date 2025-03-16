# WSGI config for dystopia project

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dystopia.settings')

application = get_wsgi_application()
