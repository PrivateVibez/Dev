"""
Django settings for privatevibez project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import django
from django.utils.encoding import force_str, smart_str
django.utils.encoding.force_text = force_str
django.utils.encoding.smart_text = smart_str
import os, datetime
from pickle import TRUE
from django.core.management.utils import get_random_secret_key





# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = '*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', default=0)))

ALLOWED_HOSTS = [
    '127.0.0.1',
    '127.0.0.1:',
    'dev.privatevibez.com',
    'localhost',
    'privatevibez.com',
    'wss://privatevibez.com'
    ]

# Application definition

INSTALLED_APPS = [

    'cities',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    "channels",
    'base.apps.BaseConfig',
    'accounts.apps.AccountsConfig',
    'staff.apps.StaffConfig',
    'rooms.apps.RoomsConfig',
    'chat.apps.ChatConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
CORS_ALLOW_ALL_ORIGINS = True

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'privatevibez.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

AUTH_USER_MODEL = 'accounts.CustomUser'

GEOS_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libgeos_c.so.1'

GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'

SESSION_COOKIE_AGE = 30 * 24 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

WSGI_APPLICATION = 'privatevibez.wsgi.application'
ASGI_APPLICATION = 'privatevibez.asgi.application'
CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'privatevibez',
        'USER': 'privatevibez',
        'PASSWORD': 'privatevibez',
        'HOST': 'db',
        'PORT': '5432',
    }
}

FERNET_KEY = "m331EIweQea4aq9DVOAtTSD-aF78PEVqMIjLBeSyyq8="

LOVENSE_DEV_KEY = "0jB878HkDC38YdjJCDkfDMfdVIDrip3HPMrax15qfobD4Y-g4p54nAgEJWr7NZsx"

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

STAFF_WITH_PROMOTION_REGISTRATION_LINK = f'http://127.0.0.1:8000/accounts/BroadcasterRegistration/'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'info@360parrot.com'
# EMAIL_HOST_PASSWORD = 'qwerty123456'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '4834fd826b3437'
EMAIL_HOST_PASSWORD = 'f524e25b102650'
EMAIL_PORT = '2525'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# aws settings
AWS_ACCESS_KEY_ID = 'AKIA3S432HUVR7JMRD3K'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'privatevibez'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'



# Pagination configuration
PAGINATION_DEFAULT_PAGINATION = 20
