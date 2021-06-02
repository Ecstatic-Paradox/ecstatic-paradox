from django.contrib import admin
from wagtail.core.models import Page

from .models import HomePage

admin.site.register(HomePage)
admin.site.register(Page)
