import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw_dj.settings_gateway')

application = get_wsgi_application()
