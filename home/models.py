# from typing_extensions import Required
from django import forms
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db.models import constraints

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
from wagtail.admin.forms import WagtailAdminPageForm
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
    date_of_birth = models.DateField(blank=True, null=True)

    # Also update at settings and forms html
    @property
    def is_attended_today(self):
        AttendanceIssue = apps.get_model(app_label="home", model_name="AttendanceIssue")
        Attendance = apps.get_model(app_label="home", model_name="Attendance")
        try:
            today_attendance_issue = AttendanceIssue.objects.get(
                date__lte=datetime.date.today(), is_open=True
            )
        except Exception:
            return False
        return bool(
            Attendance.objects.filter(
                issue_date=today_attendance_issue, member=self
            ).count()
        )

    @property
    def has_unrecorded_leave(self):
        Absentee = apps.get_model(app_label="home", model_name="Absentee")

        return bool(Absentee.objects.filter(member=self).filter(remarks="").count())


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

    date = models.DateTimeField(unique=True)
    remarks = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    def save(self, *args, **kwrgs):
        if self.is_open:
            try:
                tmp_arr = AttendanceIssue.objects.filter(is_open=True)
                for tmp in tmp_arr:
                    if self != tmp:
                        tmp.is_open = False
                        tmp.save()
            except AttendanceIssue.DoesNotExist:
                pass

        super(AttendanceIssue, self).save(*args, **kwrgs)

    def __str__(self):
        return str(self.date)

    def get_absentee_list(self):
        Attendance = apps.get_model(app_label="home", model_name="Attendance")
        Absentee = apps.get_model(app_label="home", model_name="Absentee")
        return User.objects.exclude(
            models.Q(attendance__in=Attendance.objects.filter(issue_date=self))
            | models.Q(absentee__in=Absentee.objects.filter(issue_date=self))
        )

    class Meta:
        permissions = [
            ("manage_attendance", "Can Manage Attendance System"),
        ]



class Attendance(models.Model):
    """Record attendance of each day"""

    issue_date = models.ForeignKey(AttendanceIssue, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        constraints= [
            models.UniqueConstraint(fields=['issue_date', 'member'], name="unique member and issue_date")
        ]

class Absentee(models.Model):
    """Record list of reasons absentees(without informing HR)"""

    issue_date = models.ForeignKey(AttendanceIssue, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    is_filled = models.BooleanField(default=False)

class AskForLeaveMember(models.Model):
    """ People who asked for leave  """

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    is_approved = models.BooleanField(default=False)










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

    api_fields = [
        APIField("date"),
        APIField("title"),
        APIField("description"),
        APIField("thumbnail"),
        APIField("youtube_link"),
        APIField("registration_form"),
    ]


class Symposium(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="Symposium_thumbnails")
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

    api_fields = [
        APIField("date"),
        APIField("title"),
        APIField("description"),
        APIField("thumbnail"),
        APIField("youtube_link"),
        APIField("registration_form"),
    ]


class Course(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="course_thumbnails")
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

    api_fields = [
        APIField("date"),
        APIField("title"),
        APIField("description"),
        APIField("thumbnail"),
        APIField("youtube_link"),
        APIField("registration_form"),
    ]



class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    date_published = models.DateField()
    research_paper_file = models.FileField(upload_to='research_papers', null=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("author"),
        FieldPanel("date_published"),
        FieldPanel("paper_file")
    ]


    api_fields = [
        APIField("title"),
        APIField("date_published"),
        APIField("author"),
        APIField("paper_file"),
    ]


class Project(models.Model):
    title = models.CharField(max_length=30)
    overview = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    thumbnail = models.ImageField()
    description = models.TextField()
    is_highlight = models.BooleanField()
    is_completed = models.BooleanField()

    api_fields = [
        APIField("title"),
        APIField("start_date"),
        APIField("end_date"),
        APIField("description"),
        APIField("thumbnail"),
        APIField("is_highlight"),
        APIField("is_completed"),
    ]



class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=30)
    duration = models.CharField(max_length=20)
    overview = models.TextField()
    minute = models.TextField()
    minute_file = models.FileField(upload_to="minute_file")


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
    # API configuration
    api_fields = [
        APIField("date_published"),
        APIField("content"),
        APIField("sections"),
        APIField("author"),
    ]
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


@register_snippet
class Notification(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    message = models.TextField()
    has_expired = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
