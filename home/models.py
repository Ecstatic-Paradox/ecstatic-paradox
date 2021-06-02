from django import forms
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser

from wagtail.core.models import Page

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.api import APIField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.models import register_snippet

import datetime


class HomePage(Page):
    pass


class User(AbstractUser):
    """Store General information about user and also handle auth."""

    country = models.CharField(max_length=20)
    address = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=20)
    user_department = models.ForeignKey(
        "home.Department", on_delete=models.SET_NULL, null=True, blank=True
    )
    institution = models.CharField(max_length=1000, blank=True, null=True)
    fb_profile_link = models.CharField(max_length=1000, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    @property
    def is_attended_today(self):
        AttendanceIssue = apps.get_model(app_label="home", model_name="AttendanceIssue")
        Attendance = apps.get_model(app_label="home", model_name="Attendance")
        try:
            today_attendance_issue = AttendanceIssue.objects.get(
                date=datetime.date.today()
            )
        except Exception:
            return False
        return bool(
            Attendance.objects.filter(
                issue_date=today_attendance_issue, member=self
            ).count()
        )


#     # def unrecorded_leave(self):
#     #     AttendanceIssue = apps.get_model(app_label='home', model_name='AttendanceIssue')
#     #     Attendance = apps.get_model(app_label='home', model_name='Attendance')
#     #     Absentee = apps.get_model(app_label='home', model_name='Absentee')

#     #     if AttendanceIssue


@register_snippet
class Department(models.Model):
    department_title = models.CharField(max_length=30)
    hod = models.ForeignKey(
        "home.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.department_title


class AttendanceIssue(models.Model):
    """Record which days attendance was opened by HR"""

    date = models.DateField(unique=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(null=True)

    def __str__(self):
        return str(self.date)

    # To do-->Add validation for the User (must be HR)


class Attendance(models.Model):
    """Record attendance of each day"""

    issue_date = models.ForeignKey(AttendanceIssue, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()
    remarks = models.TextField(null=True)


class Absentee(models.Model):
    """Record list of reasons absentees(without informing HR)"""

    issue_date = models.ForeignKey(AttendanceIssue, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField()


class Webinar(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="webinar_thumbnails")
    youtube_link = models.TextField()
    registration_form = models.TextField()

    panels = [
        FieldPanel("date"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("thumbnail"),
        FieldPanel("youtube_link"),
        FieldPanel("registration_form"),
    ]


class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    date_published = models.DateField()
    panels = [
        FieldPanel("title"),
        FieldPanel("author"),
        FieldPanel("date_published"),
    ]


class Notice(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    issuer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    attachment = models.FileField(upload_to="notice_attachments")
    is_pinned = models.BooleanField()
    expiry_date = models.DateTimeField()

    @property
    def is_expired(self):
        return True


class Project(models.Model):
    title = models.CharField(max_length=30)
    overview = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    thumbnail = models.ImageField()
    description = models.TextField()
    is_highlight = models.BooleanField()
    is_completed = models.BooleanField()


class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=30)
    duration = models.CharField(max_length=20)
    overview = models.TextField()
    minute = models.TextField()


class Article(Page):
    date_published = models.DateTimeField()
    content = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock(icon="image")),
            ("embedded_video", EmbedBlock(icon="media")),
        ],
        null=True,
        blank=True,
    )
    sections = ParentalManyToManyField("home.PublicationSection", blank=True)
    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField("content"),
        # index.SearchField("author"),
        index.FilterField("date_published"),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        # FieldPanel("author"),
        StreamFieldPanel("content", classname="full"),
        FieldPanel("sections", widget=forms.CheckboxSelectMultiple),
    ]
    parent_page_types = ["home.HomePage"]

    @property
    def author(self):
        return self.owner.get_full_name()


# ---------------------Categories
class CustomSection(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"


@register_snippet
class ProgramSection(CustomSection):
    pass


@register_snippet
class PublicationSection(CustomSection):
    pass


@register_snippet
class CourseSection(CustomSection):
    pass


@register_snippet
class ProjectSection(CustomSection):
    pass
