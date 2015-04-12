"""
Django settings for pinder project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6_97r5r@htf9lmlg_25=kck-0&@icz=3=f8et*bcd50f19jf#t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pinder',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django_facebook.context_processors.facebook',
    'django.contrib.auth.context_processors.auth',
    'pinder.context_processors.static_vars',
)
TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
ROOT_URLCONF = 'pinder.urls'
WSGI_APPLICATION = 'pinder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


FACEBOOK_APP_ID = "702303806446281"
FACEBOOK_APP_SECRET = "ee2a881823f96c2825735b6dddef50e9"
FB_AUTH_REDIRECT = "http://localhost:8000/auth/facebook/"


HERE_APP_ID = "BesTRPqhaKlwoC5VjDEi"
HERE_APP_CODE = "Qdg6JhSEv5Iy4o8Wg6-rYw"

# Celery Settings
BROKER_URL = 'amqp://guest:guest@%s//' % ('localhost')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S %p"
        },
    },
    'handlers': {
        'file-main': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/main.log'
        },
        'file-tasks': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/tasks.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # 'views': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # },
        # 'tasks': {
        #     'handlers': ['file-tasks'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # }
    }
}


#########################################################
# SMS Settings
#########################################################
CHIKKA_ID = "2064f98f6b0ee4b945affe221173fd499324054bf5be699bf4b22b62d81b985d"
CHIKKA_KEY = "4ed703df25237171ca8c36da85e2e458bfa2694a79616c0cdc06caad82cddc78"
CHIKKA_SHORT_CODE = "29290619"
