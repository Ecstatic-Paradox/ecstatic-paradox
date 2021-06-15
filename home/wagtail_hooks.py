from django.urls import reverse
from django.urls import path, reverse
from django.utils.html import format_html
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.db.models import Q
from django.http.response import HttpResponseRedirect

from wagtail.admin.views.account import BaseSettingsPanel
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)


from .views import TodayAttendance, AttendanceIssueInspect, MarkMemberOnLeaveView, AskMemberReasonView
from .models import (
    Attendance,
    Absentee,
    Course,
    HomePage,
    AttendanceIssue,
    Article,
    Symposium,
    Webinar,
    ResearchPaper,
    Project,
    Notification,
)
from .forms import CustomProfileSettingsForm

import datetime


# Customize account settings
@hooks.register("register_account_settings_panel")
class CustomSettingsPanel(BaseSettingsPanel):
    name = "profile"
    title = "My profile"
    order = 290
    form_class = CustomProfileSettingsForm
    form_object = "user"


# Add notifications page in Dashboard Home
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
    menu_items[:] = [i for i in menu_items if (i.label not in ["Pages"])]
    
    return HttpResponseRedirect('/today-attendance')
    pass


# ----------------- Today's Attendace Related --------------------------
hooks.register(
    "register_admin_urls",
    lambda: [
        path("today-attendance/", TodayAttendance.as_view(), name="today-attendance"),
        path('mark-member-on-leave/', MarkMemberOnLeaveView.as_view(), name="mark-member-on-leave"),
        path('ask-member-reason/', AskMemberReasonView.as_view()),
    ],
)


class TodayAttendanceMenuItem(MenuItem):
    """Show Today's Attendance Menu option only if user isnot attended and attendance is issued that day"""

    def is_shown(self, request):
        return ((not request.user.is_attended_today) and bool(
            AttendanceIssue.objects.filter(is_open=True).count()
        ))


@hooks.register("register_admin_menu_item")
def register_today_attendance():
    return TodayAttendanceMenuItem(
        "Today's Attendence",
        reverse("today-attendance"),
        classnames="icon icon-date",
    )


# Custom Dashboard Options register


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
    list_display = (
        "issue_date",
        "member",
        "status"
    )
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
    list_filter = ("date", )
    search_fields = ("date", "remarks")
    inspect_view_enabled=True
    inspect_view_class = AttendanceIssueInspect
    inspect_view_fields = ['date', 'remarks', 'is_open', ]

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


class AttendanceAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Attendance"
    menu_order = 700
    items = (AttendanceAdmin, AttendanceIssueAdmin, AbsenteeListAdmin)


modeladmin_register(AttendanceAdminGroup)


class WebinarAdmin(ModelAdmin):
    model = Webinar
    menu_label = "Webinar"
    menu_icon = "pilcrow"
    list_display = ("title", "date")
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
    items = (WebinarAdmin,SymposiumAdmin)


modeladmin_register(ProgramsAdminGroup)


class ProjectAdmin(ModelAdmin):
    model = Project
    menu_icon = "folder-inverse"
    menu_label = "Projects"
    menu_order = 700
    list_display = ("title", "start_date", "end_date")
    search_fields = ("title", "overview", "description")
    list_filter = (
        "is_highlight",
        "is_completed",
    )


modeladmin_register(ProjectAdmin)

class CourseAdmin(ModelAdmin):
    model = Course
    menu_icon = "folder-inverse"
    menu_label = "Courses"
    menu_order = 700
    list_display = ("title", "date",)
    search_fields = ("title", "date","description")


modeladmin_register(CourseAdmin)
