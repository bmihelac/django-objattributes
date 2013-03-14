import os.path

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'django_extensions',

    'core',
    'objattributes',
]

SITE_ID = 1

ROOT_URLCONF = "urls"

DEBUG = True

SECRET_KEY = "SECRET_KEY"

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'database.db'),
    }
}
