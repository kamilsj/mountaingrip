import os
import django_heroku

db = []
aws = []
email = []
gmaps_key =[]

if os.getenv('DB_NAME') and os.getenv('AWS_KEY') and os.getenv('EMAIL_HOST') and os.getenv('GMAPS'):
    db = [os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_PORT')]
    aws = [os.getenv('AWS_KEY'), os.getenv('AWS_PASSWORD'),  os.getenv('AWS_BOTTLE')]
    email = [os.getenv('EMAIL_HOST'), os.getenv('EMAIL_NAME'), os.getenv('EMAIL_PASSWORD'), os.getenv('EMAIL_PORT')]
    gmaps_key = [os.getenv('GMAPS')]
else:
    try:
        from .config.config import db, aws, email, gmaps_key, secret_key
    except ImportError:
        exit('No configuration')

GKEY = gmaps_key[0]

if os.getenv('PROD'):
    prod = os.getenv('PROD')
else:
    prod = 0

if os.getenv('SECRET_KEY'):
    SECRET_KEY = os.getenv('SECRET_KEY')
else:
    SECRET_KEY = secret_key[0]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if prod == 0:
    DEBUG = True
else:
    DEBUG = False
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn="https://ed78ed6f47e44d95b3fe18f9bf3c5cc1@sentry.io/1377157",
        integrations=[DjangoIntegration()]
    )

ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'groups',
    'notifications',
    'inbox',
    'start',
    'api',
    'rest_framework',
    'django_countries',
    'birthday',
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
USE_TZ = False

TIME_ZONE = 'Europe/Warsaw'


# Static files (CSS, JavaScript, Images)

django_heroku.settings(locals())


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