"""
Django settings for marssite project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#!import warnings
#!
#!warnings.filterwarnings(
#!    'error', r"DateTimeField .* received a naive datetime",
#!    RuntimeWarning, r'django\.db\.models\.fields',
#!)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

LOGIN_URL = "/admin/login/"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#MEDIA_ROOT = '/var/mars/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'bower_components'),
    os.path.join(BASE_DIR, 'theme'),
    #os.path.join(BASE_DIR, 'sass_out'),
    #os.path.join(BASE_DIR, 'schedule', 'static')
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#STATIC_ROOT = '/var/www/mars/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'siap',
    'docs',
    'schedule',
    'provisional',
    'water',
    'tada',
    'lsa',  # Legacy Science Archive (pre-NATICA)
    'natica', # replace LSA
    'portal',
    'rest_framework',
    'rest_framework_swagger',
    'django_tables2',
    'audit',  # tada audit/status REST API
)



#! MIDDLEWARE_CLASSES = (
#!     'django.contrib.sessions.middleware.SessionMiddleware',
#!     'django.middleware.common.CommonMiddleware',
#!     'django.middleware.csrf.CsrfViewMiddleware',
#!     'django.contrib.auth.middleware.AuthenticationMiddleware',
#!     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#!     'django.contrib.messages.middleware.MessageMiddleware',
#!     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#!     'django.middleware.security.SecurityMiddleware',
#!     'django.contrib.admindocs.middleware.XViewMiddleware',
#! )
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'dal.middleware.RequestExceptionHandler',
    ]

ROOT_URLCONF = 'marssite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'marssite.context_processors.project_status',
                #'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'marssite.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'MST'
USE_I18N = True
USE_L10N = True
USE_TZ = True


SWAGGER_SETTINGS = {
#!    'exclude_namespaces': [],
#!    'api_version': '0.1',
#!    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
#!        'put',
#!        'patch',
#!        'delete'
    ],
#!    'api_key': '',
#!    'is_authenticated': False,
#!    'is_superuser': False,
#!    'permission_denied_handler': None,
#!    'resource_access_handler': None,
#!    'base_path':'localhost:8000/docs',
    'info': {
        'title': 'MARS Prototype API Documentation',
        'description': ('This is documentation for the '
                        'MARS (Metadata Archive Retrival Services) '
                        'prototype server.  '
                        # '<br />'
                        # 'You can find out more about Swagger at '
                        # '<a href="http://swagger.wordnik.com">'
                        # 'http://swagger.wordnik.com</a> '
                        # 'or on irc.freenode.net, #swagger. '
        ),
#        'license': 'Apache 2.0',
#        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
#!    #! 'doc_expansion': 'none',
#!    'doc_expansion': 'full',
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    #!'DEFAULT_PERMISSION_CLASSES': [
    #!    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    #!]
}


CONN_MAX_AGE = 7200 # keep DB connections for 2 hours


if 'TRAVIS' not in os.environ:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        #!'formatters': {
        #!    'django.server': {
        #!        '()': 'django.utils.log.ServerFormatter',
        #!        'format': '[%(server_time)s] %(message)s',
        #!    }
        #!},
        'formatters': {
            'brief': {
                'format': '%(levelname)-8s: %(filename)-17s: %(message)s',
            },
            'precise': {
                'format': '%(asctime)s %(filename)-17s %(levelname)-8s %(message)s',
            },
        },
        'handlers': {
            'file': {
                'class' : 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'precise',
                'filename': '/var/log/mars/mars.log',
                #! 'maxBytes': 10000000,
                #! 'backupCount': 5,
            },
            'debugfile': {
                'class' : 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'precise',
                'filename': '/var/log/mars/mars-detail.log',
                #! 'maxBytes': 10000000,
                #! 'backupCount': 5,
            },
            #!'django.server': {
            #!    'level': 'INFO',
            #!    'class': 'logging.StreamHandler',
            #!    'formatter': 'django.server',
            #!},
        },
        'root': {
            'handlers': ['file', 'debugfile'],
            'level': 'DEBUG',
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'debugfile'],
                'level': 'DEBUG',
                'propagate': True,
            },
            #!'django.server': {
            #!    'handlers': ['django.server'],
            #!    'level': 'INFO',
            #!    'propagate': False,
            #!}
        },
    }

# Get DB connection info
#from .settings_local import *
if 'TRAVIS' in os.environ:
    DEBUG=True
    SECRET_KEY = 'z9z^f+lzkzt3#9iq-0p_ufigb(4oqbtk@(okc#bjdb_cottx0)'
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'travisci',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
else:
    exec(open('/etc/mars/django_local_settings.py').read())
