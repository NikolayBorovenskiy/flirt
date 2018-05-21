# coding: utf-8

import dj_database_url

from dating.settings.base import *

ADMINS = ()

MANAGERS = ()

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.parse(e.get('DJANGO_DB')),
}


# Wrap loaders in cached loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(MANAGE_DIR, 'cache'),
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

DEFAULT_FROM_EMAIL = e.get('DJANGO_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = e.get('DJANGO_EMAIL_HOST')
EMAIL_PORT = e.get('DJANGO_EMAIL_PORT')
EMAIL_HOST_USER = e.get('DJANGO_EMAIL_USER')
EMAIL_HOST_PASSWORD = e.get('DJANGO_EMAIL_PASSWORD')
EMAIL_USE_TLS = e.get('DJANGO_EMAIL_USE_TLS')
EMAIL_USE_SSL = e.get('DJANGO_EMAIL_USE_SSL')
EMAIL_SUBJECT_PREFIX = 'dating '

