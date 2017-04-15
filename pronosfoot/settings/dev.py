from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  #provide your host name

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# CSRF_COOKIE_DOMAIN = ''
# CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
