from ecstaticparadox.settings.dev import ALLOWED_HOSTS
from .base import *
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
ALLOWED_HOSTS = ['app.ecstaticparadox.com', 'ecstaticparadox.com']
CORS_ORIGIN_WHITELIST = ("https://ecstaticparadox.com",)
WAGTAILAPI_BASE_URL = "https://app.ecstaticparadox.com"


MEDIA_ROOT = os.path.join(BASE_DIR, "../app.ecstaticparadox.com/media")
try:
    from .local import *
except ImportError:
    pass
