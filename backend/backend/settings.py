"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django.conf.locale

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='id2!=m#1+zn$u@cs=f)7*e90kb8#-@wo7wbb(1c$smd3@se8bu')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', default='off') == 'on'

ALLOWED_HOSTS = ['127.0.0.1', 'antivirus.el.kg']

# Application definition

INSTALLED_APPS = [
    'jet',
    "modeltranslation",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'distributor',
    'rangefilter',
    'rest_framework',
    'django_extensions',
    'django_filters',
    'corsheaders',
    'cacheops',
    'rest_framework_recaptcha',
    'leaflet'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DISTRIBUTOR_DB_NAME', 'distributor'),
        'USER': os.environ.get('DISTRIBUTOR_DB_USER', 'master'),
        'PASSWORD': os.environ.get('DISTRIBUTOR_DB_PASSWORD'),
        'HOST': os.environ.get('DISTRIBUTOR_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DISTRIBUTOR_DB_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'  # язык сайта по умолчанию

EXTRA_LANG_INFO = {
    'ky': {
        'bidi': False,
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': u"Кыргызча",
    },
}

django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LANGUAGES = (
    ('ru', 'Russian'),
    ('ky', 'Kyrgyz'),
)

USE_I18N = True  # активация системы перевода django

# месторасположение файлов перевода
LOCALE_PATHS = (
    'locale',
    # os.path.join(PROJECT_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', default=os.path.join(BASE_DIR, "assets"))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# Cors configurations

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
    'POST',
)

CORS_PREFLIGHT_MAX_AGE = 86400

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

CACHEOPS_REDIS = "redis://{REDIS_HOST}:{REDIS_PORT}/1".format(REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT)

CACHEOPS_DEFAULTS = {
    'timeout': 7200  # 2 hours
}

CACHEOPS = {
    'distributor.hospital': {'ops': 'get', 'timeout': 3600},
    'distributor.locality': {'ops': 'get', 'timeout': 3600},
    'distributor.district': {'ops': 'get', 'timeout': 3600},
    'distributor.region': {'ops': 'get', 'timeout': 3600},
}

# JET Admin configurations

JET_DEFAULT_THEME = 'light-gray'
JET_SIDE_MENU_COMPACT = True

DRF_RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

X_FRAME_OPTIONS = 'SAMEORIGIN'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (42.870026, 74.599795),
    'DEFAULT_ZOOM': 12,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
}

if os.environ.get('ENABLE_LOGGING', default='off') == 'on':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': '/var/log/django/error.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
