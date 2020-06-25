import os
import django_heroku

db = ['']
aws = ['']
email = ['']

if os.getenv('DB_NAME') and os.getenv('AWS_KEY') and os.getenv('EMAIL_HOST'):
    db[0] = os.getenv('DB_NAME')
    db[1] = os.getenv('DB_USER')
    db[2] = os.getenv('DB_PASSWORD')
    db[3] = os.getenv('DB_HOST')
    db[4] = os.getenv('DB_PORT')
    aws[0] = os.getenv('AWS_KEY')
    aws[1] = os.getenv('AWS_PASSWORD')
    aws[2] = os.getenv('AWS_BOTTLE')
    email[0] = os.getenv('EMAIL_HOST')
    email[1] = os.getenv('EMAIL_NAME')
    email[2] = os.getenv('EMAIL_PASSWORD')
    email[3] = os.getenv('EMAIL_PORT')
else:
    try:
        from .config.config import db, aws, email
    except ImportError:
        exit('No configuration')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q4nyffh4o&gd^=s-rkkc^fw%^k(0u#f7#fk=5+6bjz-hjom27y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'start',
    'api',
    'rest_framework',
    'django_countries',
    'django_cron',
    'widget_tweaks',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
CRON_CLASSES = [
    'start.LearnYourself'
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mountaingrip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/html/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mountaingrip.wsgi.application'


# Database


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db[0],
        'USER': db[1],
        'PASSWORD': db[2],
        'HOST': db[3],
        'PORT': db[4]
    }
}


# Password validation

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

LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'UTC'


# Static files (CSS, JavaScript, Images)

django_heroku.settings(locals())

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://ed78ed6f47e44d95b3fe18f9bf3c5cc1@sentry.io/1377157",
    integrations=[DjangoIntegration()]
)



# My settings

AUTHENTICATION_BACKENDS = {
    'django.contrib.auth.backends.ModelBackend',
}


LOGIN_REDIRECT_URL = '/start/'
LOGOUT_REDIRECT_URL = '/'

#S3
AWS_DEFAULT_ACL = 'public-read'
AWS_AUTO_CREATE_BUCKET = True
AWS_ACCESS_KEY_ID = aws[0]
AWS_SECRET_ACCESS_KEY = aws[1]
AWS_STORAGE_BUCKET_NAME = aws[2]
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'data'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'html/static/'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'mountaingrip.storage.MediaStorage'

#Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = email[0]
EMAIL_HOST_USER = email[1]
EMAIL_HOST_PASSWORD = email[2]
EMAIL_PORT = email[3]