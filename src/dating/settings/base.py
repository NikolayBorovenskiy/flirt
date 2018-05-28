# coding: utf-8
"""
Settings for dating project.
"""

import os
import sys

import envvars as e
from django.contrib.messages import constants as messages

PROJECT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
MANAGE_DIR = os.path.normpath(os.path.join(PROJECT_DIR, '..'))
ROOT_DIR = os.path.normpath(os.path.join(MANAGE_DIR, '..'))

e.load(os.path.join(ROOT_DIR, 'conf/env'))

SECRET_KEY = e.get('DJANGO_SECRET')

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # third-party apps
    'allauth',
    'allauth.account',
    'cmstemplates',
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',
    'el_pagination',
    'easy_thumbnails',
    'django_cleanup',
    'django_countries',

    # project apps
    'core',
    'accounts',
    'bookmarks',
    'chat',
    'notifications_service',
]

AUTH_USER_MODEL = 'accounts.DatingUser'

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]
# CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

SITE_ID = 1

ROOT_URLCONF = 'dating.urls'

WSGI_APPLICATION = 'dating.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

FIRST_DAY_OF_WEEK = 1

USE_TZ = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': (
                # django builtin processors
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ),
            'libraries': {},
            'builtins': [
                'rules.templatetags.rules',

                'core.templatetags.builtins',
                'el_pagination.templatetags.el_pagination_tags',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        }
    },
]

LOCALE_PATHS = [
    os.path.abspath(os.path.join(PROJECT_DIR, 'locale')),
]

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
    ('img', os.path.join(STATIC_ROOT, 'img')),
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
    ('fonts', os.path.join(STATIC_ROOT, 'fonts')),
    ('vendor', os.path.join(STATIC_ROOT, 'vendor')),
    ('build', os.path.join(STATIC_ROOT, 'build')),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

COOKIE_HTTP_ONLY = True

CSRF_COOKIE_NAME = '__csrf'

CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

LANGUAGE_COOKIE_NAME = '__lang'

SESSION_COOKIE_NAME = '__sid'

USE_ETAGS = False

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SECURE_BROWSER_XSS_FILTER = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'logfile': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(ROOT_DIR, 'var/log/error.log'),
            'when': 'D',
            'backupCount': 10,
        },
        'stdout': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'message-delivery': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# debug toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# django-allauth
# ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_ADAPTER = "accounts.adapters.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_FORMS = {}
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_FORM_CLASS = "accounts.forms.UserCreationForm"
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True  # одно поле для пароля
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'administrator', 'superuser']
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_PASSWORD_MIN_LENGTH = 3
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# django-cmstemplates
CMSTEMPLATES_USE_CODEMIRROR = True

# django-codemirror-widget
CODEMIRROR_PATH = 'vendor/codemirror'
CODEMIRROR_THEME = 'default'
CODEMIRROR_CONFIG = {'lineNumbers': True}

# django-ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = os.path.join(STATIC_URL,
                                   'vendor/jquery/dist/jquery.min.js')
CKEDITOR_RESTRICT_BY_USER = True

# CKEDITOR_CONFIGS = {
#    'default': {}
# }

# celery
# таймаут для задач - 1 минута
CELERYD_TASK_SOFT_TIME_LIMIT = 60
BROKER_URL = e.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = e.get('CELERY_RESULT_BACKEND')

# pymorphy
import pymorphy2

MORPH = pymorphy2.MorphAnalyzer()
