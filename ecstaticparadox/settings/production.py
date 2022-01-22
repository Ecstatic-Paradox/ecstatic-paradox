from ecstaticparadox.settings.dev import ALLOWED_HOSTS
from .base import *
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ALLOWED_HOSTS = ['app.ecstaticparadox.com', 'ecstaticparadox.com']
CORS_ORIGIN_WHITELIST = ("https://ecstaticparadox.com", "https://www.ecstaticparadox.com")
WAGTAILAPI_BASE_URL = "https://app.ecstaticparadox.com"
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 3153600
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "mail.ecstaticparadox.com"
EMAIL_HOST_USER = "noreply@ecstaticparadox.com" 
EMAIL_HOST_PASSWORD =  os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MEDIA_ROOT = os.path.join(BASE_DIR, "../app.ecstaticparadox.com/media")
try:
    from .local import *
except ImportError:
    pass
