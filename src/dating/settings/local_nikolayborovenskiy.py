# coding: utf-8

import os
from dating.settings.base import *

DEBUG = True

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# DATABASES = {
#     'default': dj_database_url.parse(e.get('DJANGO_DB')),
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache_dating',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = e.get('DJANGO_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = e.get('DJANGO_EMAIL_HOST')
EMAIL_PORT = e.get('DJANGO_EMAIL_PORT')
EMAIL_HOST_USER = e.get('DJANGO_EMAIL_USER')
EMAIL_HOST_PASSWORD = e.get('DJANGO_EMAIL_PASSWORD')
EMAIL_USE_TLS = e.get('DJANGO_EMAIL_USE_TLS')
EMAIL_USE_SSL = e.get('DJANGO_EMAIL_USE_SSL')
EMAIL_SUBJECT_PREFIX = 'dating '

INTERNAL_IPS = ['127.0.0.1']
