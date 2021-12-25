# from typing_extensions import Required
from django import forms
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db.models import constraints
from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.core.models import Page
from wagtail.users.models import UserProfile

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
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.forms import WagtailAdminPageForm
import datetime
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager


class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'id': value.id,
                'title': value.title,
                'large': value.get_rendition('width-1000').attrs_dict,
                # 'thumbnail': value.get_rendition('fill-120x120').attrs_dict,
            }

class HomePage(Page):
    """Wagtail Base Parent Page class for other Page Classes"""

    pass


class User(AbstractUser):
    """Store General information about user and also handle auth."""

    # First Name, Last Name, Email, Username, Password From Abstract Class.
    # Access Profile picture through user.wagtail_userprofile.avatar (Provided in post_save )
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
    designation = models.CharField(
        max_length=1000, default="Member", blank=True, null=True
    )
    gender = models.BooleanField(null=True, blank=True,)
    is_core_member = models.BooleanField(default=True)
    # If any updates is made in the User fields then also update at settings.py "WAGTAIL_USER_CUSTOM_FIELDS"
    # and CustomProfileSettingsForm on form.py  and templates on wagtailusers\users\create.html & edit.html
    # In order make the fields editable through Wagtail settings.

    def __str__(self) -> str:
        return "User: {} ".format(self.first_name)

    def get_unattended_issue(self):
        """Returns Open Attendance issue not attended by user"""

        AttendanceIssue = apps.get_model(app_label="home", model_name="AttendanceIssue")
        Attendance = apps.get_model(app_label="home", model_name="Attendance")

        try:
            open_issue = AttendanceIssue.objects.get(is_open=True)

        except AttendanceIssue.DoesNotExist:
            return None

        try:  # Check if user has attendance record for open issue
            attendance_record = Attendance.objects.get(
                issue_date=open_issue, member=self
            )
            return None  # return none if user has attended

        except Attendance.DoesNotExist:
            return open_issue  # return Open Attendance issue if user has not attended

    @property
    def has_unrecorded_leave(self):
        """Returns if user has any unrecorded leave and blocks all permission for user."""
        Absentee = apps.get_model(app_label="home", model_name="Absentee")

        state = bool(
            Absentee.objects.filter(member=self).filter(remarks=None).count()
        )  # Stores True if user has unrecorded leave.

        # print("\n\n\n {}: {} \n\n\n".format(state, self))
        if state:
            # If user is absent then remove her from all the groups (admin_access permission)
            # and create a new group with name "oldgrp1_oldgrp2_absentee" so that later she can be reassign to her old groups.
            if not bool(
                [group.name for group in self.groups.all() if "absentee" in group.name]
            ):  # do only if user already is not in absentee group
                new_group_name = (
                    "_".join([group.name for group in self.groups.all()]) + "_absentee"
                )
                try:
                    new_group = Group.objects.get(name=new_group_name)
                except Group.DoesNotExist:
                    new_group = Group.objects.create(name=new_group_name)
                    new_group.save()
                self.groups.clear()
                self.groups.add(new_group)
                self.save()
        else:
            # If user wasnot absent the make sure he is not in the absentee group and in his respective groups
            absentee_groups = [
                group for group in self.groups.all() if group.name.endswith("_absentee")
            ]

            if absentee_groups:

                for group in absentee_groups:
                    group.name.replace("absentee", "")
                    new_groups_names = group.name.split("_")
                    new_groups_names.pop()  # remove last empty element

                    for name in new_groups_names:
                        try:  # Try to find the respective group, if doesnot exists then continue
                            self.groups.add(Group.objects.get(name=name))
                        except Group.DoesNotExist:
                            continue
            self.save()
        return state

    search_fields = [index.SearchField("First Name"), index.SearchField("institution")]

    def get_absent_record(self):
        Absentee = apps.get_model(app_label="home", model_name="Absentee")

        return Absentee.objects.filter(member=self)


@receiver(post_save, sender=User, dispatch_uid="create_wagtail_userprofile")
def create_wagtail_userprofile(sender, instance, **kwargs):
    # if not "wagtail_userprofile" in dir(self): # Create olny if already doesnot exists. Else Unique constraint will Fail
    try:
        user_profile = UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()

    # This One to One relation with UserProfile provides different cool features of wagtail like Avatar, notification settings etc
    # Access Profile picture through user.wagtail_userprofile.avatar


@register_snippet
class Department(models.Model):
    """List of Departments in ecstatic paradox"""

    department_title = models.CharField(max_length=30)
    hod = models.ForeignKey(
        "home.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return "{} Department".format(self.department_title)


class AttendanceIssue(models.Model):
    """Record which days attendance was opened by HR"""

    date = models.DateField(unique=True)
    remarks = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    def save(self, *args, **kwrgs):

        if self.is_open:
            # Close every other attandance issue if new one is opened.
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
        return "Attendance Issue: {} ".format(str(self.date))

    def get_absentee_list(self):
        """Get unrecorded leave for particular issue users"""
        Attendance = apps.get_model(app_label="home", model_name="Attendance")
        Absentee = apps.get_model(app_label="home", model_name="Absentee")
        try:
            ret = User.objects.exclude(
                models.Q(attendance__in=Attendance.objects.filter(issue_date=self))
                | models.Q(absentee__in=Absentee.objects.filter(issue_date=self))
            )
        except:
            ret = None
        return ret

    class Meta:
        permissions = [
            ("manage_attendance", "Can Manage Attendance System"),
        ]


class Attendance(models.Model):
    """Record attendance of each issue. Just Like Attendance Sheet"""

    issue_date = models.ForeignKey(AttendanceIssue, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["issue_date", "member"], name="unique member and issue_date"
            )
        ]

    def __str__(self) -> str:
        return "Attendance: {} of {}".format(
            self.member.first_name, str(self.issue_date.date)
        )


class Absentee(models.Model):
    """Record list of reasons absentees(without informing HR)"""

    issue_date = models.ForeignKey(AttendanceIssue, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    is_filled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Absente: {} on {}".format(
            self.member.first_name, str(self.issue_date.date)
        )


class AskForLeaveMember(models.Model):
    """People who applied for leave"""

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Leave Request: {}".format(self.member.first_name)

    class Meta:
        permissions = [
            ("manage_attendance", "Can Manage Attendance System"),
        ]

class Collaborators(models.Model):
    title = models.CharField(max_length=40)
    icon = models.ImageField(upload_to="collaborators_icons")


class Webinar(models.Model, index.Indexed):
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
    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("description", partial_match=True),
    ]


class Symposium(models.Model, index.Indexed):
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
    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("description", partial_match=True),
    ]


class Course(models.Model, index.Indexed):
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
    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("description", partial_match=True),
    ]


class ResearchPaper(models.Model, index.Indexed):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(User)
    date_published = models.DateField()
    is_highlight = models.BooleanField(default=False)
    # is_completed = models.BooleanField()
    content = StreamField(
        [
            ("heading", blocks.CharBlock(classname="topics")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock(icon="image")),
        ],
        null=True,
        blank=True,
    )
    refrences = StreamField(
        [("refrence", blocks.CharBlock(classname="refrence"))]
     ,null=True,
        blank=True,)

    view = models.BigIntegerField(default=0)

    panels = [
        FieldPanel("title"),
        FieldPanel("author"),
        FieldPanel("date_published"),
        StreamFieldPanel("content", classname="full"),
        StreamFieldPanel("refrences", classname="full"),
    ]

    api_fields = [
        APIField("title"),
        APIField("date_published"),
        APIField("author"),
        APIField("content"),
        APIField("refrences"),
        APIField("view")
    ]

    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("author", partial_match=True),
    ]

    def __str__(self) -> str:
        return "{}".format(self.title)


class Project(models.Model, index.Indexed):
    title = models.CharField(max_length=30)
    members = models.ManyToManyField(User)
    start_date = models.DateField()
    end_date = models.DateField()
    thumbnail = models.ImageField()
    description = models.TextField()
    sections = models.ManyToManyField("home.ProjectSection", blank=True)
    slug = models.SlugField(unique=True)
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

    api_fields = [
        APIField("title"),
        APIField("start_date"),
        APIField("end_date"),
        APIField("description"),
        APIField("thumbnail"),
        APIField("sections"),
        APIField("members"),
        APIField("content"),
    ]
    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("description", partial_match=True),
        index.SearchField("content", partial_match=True),
    ]
    panels = [
        FieldPanel("title"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("members"),
        FieldPanel("description"),
        FieldPanel("thumbnail"),
        StreamFieldPanel("content", classname="full"),
        FieldPanel("sections", widget=forms.CheckboxSelectMultiple),
        FieldPanel("slug"),
    ]

    def __str__(self) -> str:
        return self.title


class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=30)
    duration = models.CharField(max_length=20)
    overview = models.TextField()
    minute = models.TextField()
    minute_file = models.FileField(upload_to="minute_file")

    def __str__(self) -> str:
        return self.title

class Gallery(models.Model):
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    panels = [
        ImageChooserPanel("thumbnail")
    ]
    api_fields = [APIField("thumbnail")]


class Article(Page):
    date_published = models.DateTimeField()
    # content is repaced by pdf_file
    # content = StreamField(
    #     [
    #         ("heading", blocks.CharBlock(classname="full title")),
    #         ("paragraph", blocks.RichTextBlock()),
    #         ("image", ImageChooserBlock(icon="image")),
    #         ("embedded_video", EmbedBlock(icon="media")),
    #     ],
    #     null=True,
    #     blank=True,
    # )

    pdf_file = models.FileField(upload_to='article_files', null=True)
    sections = ParentalManyToManyField("home.PublicationSection", blank=True)
    thumbnail = models.ImageField(upload_to='article_thumbnails', null=True)


    # API configuration
    api_fields = [
        APIField("date_published"),
        # APIField("content"),
        APIField("sections"),
        APIField("author"),
        APIField("thumbnail"),
        APIField("pdf_file"),
    ]
    # Search index configuration

    search_fields = Page.search_fields + [
        index.FilterField("date_published"),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        FieldPanel("pdf_file"),
        FieldPanel("thumbnail"),
        # FieldPanel("author"),
        # FieldPanel("slug"),

        # StreamFieldPanel("content", classname="full"),
        FieldPanel("sections", widget=forms.CheckboxSelectMultiple),
    ]
    parent_page_types = ["home.HomePage"]

    @property
    def author(self):
        return self.owner.get_full_name()

class BlogPostPage(Page):
    date_created = models.DateTimeField()
    view_count = models.PositiveBigIntegerField(default=0)
    # title = models.CharField(max_length=300, null=True)
    is_pinned = models.BooleanField(default=False)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
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
    tags = ClusterTaggableManager(through="home.PostPageTag", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date_created"),
        FieldPanel("is_pinned"),
        ImageChooserPanel("thumbnail"),
        StreamFieldPanel("content", classname="full"),
        InlinePanel("categories", label="category"),
        FieldPanel("tags"),
    ]
    api_fields = [
        APIField("view_count"),
        APIField("date_created"),
        APIField("content"),
        APIField("tags"),
        APIField("owner"),
        APIField("thumbnail"),
        APIField("is_pinned"),
        # APIField("categories"),
    ]

    parent_page_types = ["home.HomePage"]

# ---------------------Categories
class CustomSection(models.Model):
    """Sections for Blog and Articles"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = "Section"
        verbose_name_plural = "Sections"


@register_snippet
class ProgramSection(CustomSection):
    
    class Meta:
        verbose_name = "Program Section"
        verbose_name_plural = "Program Sections"
    




@register_snippet
class PublicationSection(CustomSection):
    class Meta:
        verbose_name = "Publication Section"
        verbose_name_plural = "Publication Sections"
    

@register_snippet
class CourseSection(CustomSection):
    class Meta:
        verbose_name = "Course Section"
        verbose_name_plural = "Course Sections"
    

@register_snippet
class ProjectSection(CustomSection):

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Project Section"
        verbose_name_plural = "Project Sections"
    


@register_snippet
class Notification(models.Model):
    """Notifications to show on dashboard"""

    date_added = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    message = models.TextField()
    has_expired = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


from taggit.models import Tag as TaggitTag
@register_snippet
class BlogTag(TaggitTag):
    class Meta:
        proxy = True
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"


# Intermediatary Models For Blog ---------------------------------------
class PostPageBlogCategory(models.Model):
    page = ParentalKey(
        "home.BlogPostPage", on_delete=models.CASCADE, related_name="categories"
    )
    blog_category = models.ForeignKey(
        "home.BlogCategory", on_delete=models.CASCADE, related_name="post_pages"
    )

    panels = [
        SnippetChooserPanel("blog_category"),
    ]

    class Meta:
        unique_together = ("page", "blog_category")


class PostPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPostPage", related_name="post_tags")