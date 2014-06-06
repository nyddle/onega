"""
Django settings for onega project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oy%)bah1r)xx7a2@m*bacn+^q42rt$p=fle%$kpdf6okcr1$+n'

# todo: switch in to False on production
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'easy_thumbnails',
    'captcha',
    # 'south',
    'chips',
)

CAPTCHA_FONT_SIZE = 30

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

THUMBNAIL_ALIASES = {
    '': {
        'gallery': {'size': (50, 50)},
    },
}

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'), )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chips.middlewares.SettingsMiddleware'
)

ROOT_URLCONF = 'onega.urls'

WSGI_APPLICATION = 'onega.wsgi.application'

LOGIN_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(default='postgres://uqvjzjpvptwgsq:Ho_B9vrBuDdgk3Nk19qmM4v8Ei@ec2-107-20-224-35.compute-1.amazonaws.com:5432/d5bto9e6scivbr')}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "chips.context_processors.get_settings"
)

AUTH_USER_MODEL = 'chips.Customer'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@app26061228.mailgun.org'
EMAIL_HOST_PASSWORD = '0j8v3jioz5n4'
EMAIL_PORT = 587
EMAIL_FROM = 'chips@omega.by'

try:
    from .local_settings import *
except ImportError:
    pass