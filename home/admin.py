from django.contrib import admin
from wagtail.core.models import Page

from .models import *

admin.site.register(HomePage)
admin.site.register(Page)
admin.site.register(AttendanceIssue)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ResearchPaper)
admin.site.register(Article)