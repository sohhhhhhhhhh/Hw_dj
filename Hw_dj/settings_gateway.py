from .settings import *  # Наследуем основные настройки

# Изменяем уникальные параметры для второго сервера
ROOT_URLCONF = 'gateway.urls'  # Пути для второго сервера
WSGI_APPLICATION = 'gateway.wsgi.application'  # WSGI второго сервера


DATABASES = {}
