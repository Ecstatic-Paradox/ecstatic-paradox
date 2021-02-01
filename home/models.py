from django.db import models

from modelcluster.fields import ParentalKey
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
from django.contrib.auth.models import User
import datetime
class HomePage(Page):
    pass

class AttendanceIssue(models.Model):
    """ Record which days attendance was opened by HR"""
    date = models.DateField(unique=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(null=True)

    def __str__(self):
        return str(self.date)
    #--------------------Add validation for the User (must be HR)

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


class Profile(models.Model):
    """ Store additional information about member, to be viewed in member profile """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20)
    address = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=20)

    @property
    def is_attended_today(self):
        # return False
        try:
            today_attendance_issue = AttendanceIssue.objects.get(date=datetime.date.today())
        except Exception:
            return False
        return bool(
            Attendance.objects.filter(
                issue_date=today_attendance_issue, member=self.user
            ).count()
        )



class Webinar(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date=models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="webinar_thumbnails")
    youtube_link = models.TextField()
    registration_form = models.TextField()

class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    date_published = models.DateField()
    
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
    ]
    parent_page_types = ["home.HomePage"]
    @property
    def author(self):
        return self.owner.get_full_name()
