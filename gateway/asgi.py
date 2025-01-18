import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw_dj.settings_gateway')

application = get_asgi_application()
