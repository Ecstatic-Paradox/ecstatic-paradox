from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wms3k9@i=8^sr-qzy*$6gju1kyw#psz6_)tbs64klaqeutsob#'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['localhost'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
