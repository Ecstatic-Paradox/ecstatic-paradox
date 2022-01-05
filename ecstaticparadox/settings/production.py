from ecstaticparadox.settings.dev import ALLOWED_HOSTS
from .base import *
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ALLOWED_HOSTS = ['periergia.com']
try:
    from .local import *
except ImportError:
    pass
