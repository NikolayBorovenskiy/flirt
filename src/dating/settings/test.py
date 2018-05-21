# coding: utf-8

import dj_database_url

from dating.settings.base import *

DEBUG = True

SECRET_KEY = 'test_key'

DATABASES = {
    'default': dj_database_url.parse(e.get('DJANGO_DB')),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = ['127.0.0.1']
