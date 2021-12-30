from .base import *
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
try:
    from .local import *
except ImportError:
    pass
