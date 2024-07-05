from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '127.0.0.1:8000']  #provide your host name

INSTALLED_APPS += [
    'sslserver',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pronosfoot-2024-2025.sqlite3'),
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
CSRF_COOKIE_SECURE = True

SEASON_FORECAST_MAX_DATE = datetime.datetime(2024,10,31,23,59,59)