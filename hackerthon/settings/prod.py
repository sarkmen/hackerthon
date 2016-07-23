from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DATABASE_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', 'hackathon'),
        'USER': os.environ.get('DJANGO_DATABASE_USER', 'ubuntu'),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD', 'p_rograsv'),
        'HOST': os.environ.get('DJANGO_DATABASE_HOST', '127.0.0.1'),
    }
}
