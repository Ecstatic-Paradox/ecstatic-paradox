from django.contrib import admin
from wagtail.core.models import Page

from .models import HomePage, AttendanceIssue, User, Project

admin.site.register(HomePage)
admin.site.register(Page)
admin.site.register(AttendanceIssue)
admin.site.register(User)
admin.site.register(Project)