from ecstaticparadox.settings.dev import ALLOWED_HOSTS
from .base import *
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
ALLOWED_HOSTS = ['app.ecstaticparadox.com']
CORS_ORIGIN_WHITELIST = ('ecstaticparadox.com')
try:
    from .local import *
except ImportError:
    pass
