
from .base import *

DEBUG = True

SECRET_KEY = 'dev-secret-key'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS += [
    
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
