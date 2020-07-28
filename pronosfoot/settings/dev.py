from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  #provide your host name

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pronosfoot-2020-2021.sqlite3'),
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, '_', 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CSRF_COOKIE_DOMAIN = ''
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

SEASON_FORECAST_MAX_DATE = datetime.datetime(2016,10,31,23,59,59)