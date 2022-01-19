from os import name
from django.urls import reverse
from django.urls import path, reverse
from django.utils.html import format_html
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.db.models import Q, F
from django.http.response import HttpResponseRedirect

from wagtail.admin.views.account import BaseSettingsPanel
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)


from .views import (
    FillAttendance,
    AttendanceIssueInspect,
    MarkMemberOnLeaveView,
    AddMemberasAbsent,
    ApplyForLeaveView,
    MembersListView,
    MemberInspectView

)
from .models import (
    Attendance,
    Absentee,
    BlogPostPage,
    Collaborators,
    Course,
    HomePage,
    AttendanceIssue,
    AskForLeaveMember,
    Article,
    Symposium,
    Webinar,
    ResearchPaper,
    Project,
    Notification,
    Gallery
)
from .forms import CustomProfileSettingsForm

import datetime

# Custom admin urls
hooks.register(
    "register_admin_urls",
    lambda: [
        path('members', MembersListView.as_view(), name='members' ),
        path('members/<int:pk>', MemberInspectView.as_view(), name='member-profile' ),
        path("fill-attendance/", FillAttendance.as_view(), name="fill-attendance"),
        path(
            "mark-member-on-leave/",
            MarkMemberOnLeaveView.as_view(),
            name="mark-member-on-leave",
        ),
        path(

             # this is for HR to add the absent member on the list
            "add-member-as-absent/", AddMemberasAbsent.as_view(), name="add-member-absent"
        ), 
        path("apply-for-leave/", ApplyForLeaveView.as_view(), name="apply-for-leave" ), #link to apply for leave
        
    ],
)


# Customize account settings, Add My profile section in Account Settings Panel
@hooks.register("register_account_settings_panel")
class CustomSettingsPanel(BaseSettingsPanel):
    name = "profile"
    title = "My profile"
    order = 290
    form_class = CustomProfileSettingsForm
    form_object = "user"


# Add notifications Section in Dashboard Home
class NotificationPanel:

    order = 50

    def __init__(self, request):
        self.request = request

    def render(self):
        unexpired = Notification.objects.filter(has_expired=False).filter(
            Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date=None)
        )
        expired_bool = Notification.objects.filter(has_expired=True)
        expired = (
            Notification.objects.filter(expiry_date__lte=datetime.datetime.now())
            .union(expired_bool)
            .order_by("-date_added")
        )

        if unexpired.count() == 0 and expired.count() == 0:
            return render_to_string(
                "home/home_notifications.html",
                {"notifications": False},
                request=self.request,
            )

        return render_to_string(
            "home/home_notifications.html",
            {
                "notifications": True,
                "unexpired_notifications": unexpired,
                "expired_notifications": expired,
            },
            request=self.request,
        )


@hooks.register("construct_homepage_panels")
def add_notifications_panel(request, panels):
    panels.pop(0)  # Remove the site_summary ie. Image 2, Docs 4 blah blah
    panels.append(NotificationPanel(request))


# Colors Change in Dashboard
@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/colors.css"))

# Additional Custom Css
@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/ep_css.css"))


@hooks.register("construct_main_menu")
def main_menu_edit(request, menu_items):
    """Remove Pages option from dashboard menu"""
    if HomePage.objects.all().count() == 0:
        mainpage = HomePage.objects.create(
            title="mainpage", slug="mainapp", depth=2, path="00010002"
        )
        HomePage.save(mainpage)

    if not request.user.is_superuser:
        menu_items[:] = [i for i in menu_items if (i.label not in ["Pages", "Images", "Documents", "Reports"])]
    return HttpResponseRedirect("/fill-attendance")


@hooks.register("register_admin_menu_item")
def register_ask_for_leave_menuitem():

    return MenuItem(
        "Apply For Leave",
        reverse("apply-for-leave"),
        classnames="icon icon-date",
        order=1200,
    )

@hooks.register("register_admin_menu_item")
def register_members_list_menuitem():

    return MenuItem(
        "Members",
        reverse("members"),
        classnames="icon icon-user",
        order=200,
    )

@hooks.register("before_serve_page")
def increment_view_count(page, request, serve_args, serve_kwargs):
    if page.specific_class == BlogPostPage:
        BlogPostPage.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)

# ----------------- Today's Attendace Related --------------------------


class TodayAttendanceMenuItem(MenuItem):
    """Show Today's Attendance Menu option only if user has unattended attendance issue."""

    def is_shown(self, request):
        return bool(request.user.get_unattended_issue())


@hooks.register("register_admin_menu_item")
def register_today_attendance():
    return TodayAttendanceMenuItem(
        "Open Attendence",
        reverse("fill-attendance"),
        classnames="icon icon-date",
    )


# Custom Dashboard Options (Model Admins) register


class ArticleAdmin(ModelAdmin):
    model = Article
    menu_label = "Articles"
    menu_icon = "doc-full"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "date_published", "live")
    list_filter = ("live", "date_published", "owner")
    search_fields = ("title", "date_published", "content", "owner")


class ResearchPaperAdmin(ModelAdmin):
    model = ResearchPaper
    menu_label = "Research Paper"
    menu_icon = "doc-full"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("title", "author")


class PublicationsAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Publications"
    menu_order = 700
    items = (
        ResearchPaperAdmin,
        ArticleAdmin,
    )


modeladmin_register(PublicationsAdminGroup)


class AttendanceAdmin(ModelAdmin):
    model = Attendance
    menu_label = "Attendance Sheet"
    menu_icon = "doc-full"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("issue_date", "member", "status")
    list_filter = ("issue_date", "status", "member")
    search_fields = ("member", "remarks")


class AttendanceIssueAdmin(ModelAdmin):
    model = AttendanceIssue
    menu_label = "Issue Attendance"
    menu_icon = "doc-full"
    menu_order = 400
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("date",)
    list_filter = ("date",)
    search_fields = ("date", "remarks")
    inspect_view_enabled = True
    inspect_view_class = AttendanceIssueInspect
    inspect_view_fields = [
        "date",
        "remarks",
        "is_open",
    ]


class AbsenteeListAdmin(ModelAdmin):
    model = Absentee
    menu_label = "Absentees"
    menu_icon = "doc-full"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("issue_date", "member")
    list_filter = ("issue_date", "member")
    search_fields = ("issue_date", "member", "remarks")


class AskForLeaveMemberAdmin(ModelAdmin):
    model = AskForLeaveMember
    menu_label = "Leave Applications"
    menu_icon = "doc-full"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("leave_start_date", "leave_end_date", "member", "is_approved")
    list_filter = ("member", "is_approved")
    search_fields = ("member", "remarks")


class AttendanceAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Attendance"
    menu_order = 700
    items = (
        AttendanceAdmin,
        AttendanceIssueAdmin,
        AbsenteeListAdmin,
        AskForLeaveMemberAdmin,
    )


modeladmin_register(AttendanceAdminGroup)


class WebinarAdmin(ModelAdmin):
    model = Webinar
    menu_label = "Webinar"
    menu_icon = "pilcrow"
    list_display = ("title", "program_date")
    list_filter = ("date_added",)
    search_fields = ("title", "description")


class SymposiumAdmin(ModelAdmin):
    model = Symposium
    menu_label = "Symposium"
    menu_icon = "pilcrow"
    list_display = ("title", "date")
    list_filter = ("date_added",)
    search_fields = ("title", "description")


class ProgramsAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Programs"
    menu_order = 700
    items = (WebinarAdmin, SymposiumAdmin)


modeladmin_register(ProgramsAdminGroup)


class ProjectAdmin(ModelAdmin):
    model = Project
    menu_icon = "folder-inverse"
    menu_label = "Projects"
    menu_order = 700
    list_display = ("title", "start_date", "end_date")
    search_fields = ("title", "overview", "description")
    list_filter = ("members",)


modeladmin_register(ProjectAdmin)


class CollaboratorsAdmin(ModelAdmin):
    model = Collaborators
    menu_icon = "folder-inverse"
    menu_label = "Collaborators"
    menu_order = 700

modeladmin_register(CollaboratorsAdmin)

class CourseAdmin(ModelAdmin):
    model = Course
    menu_icon = "folder-inverse"
    menu_label = "Courses"
    menu_order = 700
    list_display = (
        "title",
        "date",
    )
    search_fields = ("title", "date", "description")


modeladmin_register(CourseAdmin)

class BlogAdmin(ModelAdmin):
    model = BlogPostPage
    menu_icon = "folder-inverse"
    menu_label = "Blogs"
    menu_order = 700
    list_display = (
        "title",
    )
    search_fields = ("title", "content")


modeladmin_register(BlogAdmin)
class GalleryAdmin(ModelAdmin):
    model = Gallery
    menu_icon = "folder-inverse"
    menu_label = "Gallery"
    menu_order = 700
    list_display = (
        "thumbnail",
    )

modeladmin_register(GalleryAdmin)

