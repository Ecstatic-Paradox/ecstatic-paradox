from django.urls import reverse
from django.urls import path, reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)


from .views import TodayAttendance
from .models import (
    Attendance,
    HomePage,
    AttendanceIssue,
    Article,
    Webinar,
    ResearchPaper,
    Project,
)
import datetime


@hooks.register("construct_main_menu")
def main_menu_edit(request, menu_items):
    """Remove Pages option from dashboard menu"""
    if HomePage.objects.all().count() == 0:
        mainpage = HomePage.objects.create(
            title="mainpage", slug="mainapp", depth=2, path="00010002"
        )
        HomePage.save(mainpage)
    menu_items[:] = [i for i in menu_items if (i.label not in ["Pages"])]
    pass


# ----------------- Today's Attendace Related --------------------------
hooks.register(
    "register_admin_urls",
    lambda: [
        path("today-attendance/", TodayAttendance.as_view(), name="today-attendance")
    ],
)


class TodayAttendanceMenuItem(MenuItem):
    """Show Today's Attendance Menu option only if user isnot attended and attendance is issued that day"""

    def is_shown(self, request):
        return (not request.user.is_attended_today) and bool(
            AttendanceIssue.objects.filter(date=datetime.date.today()).count()
        )


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
    list_filter = ("date", "member")
    search_fields = ("issue_date", "remarks")


class AttendanceAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Attendance"
    menu_order = 700
    items = (AttendanceAdmin, AttendanceIssueAdmin)


modeladmin_register(AttendanceAdminGroup)


class WebinarAdmin(ModelAdmin):
    model = Webinar
    menu_label = "Webinar"
    menu_icon = "pilcrow"
    list_display = ("title", "date")
    list_filter = ("date_added",)
    search_fields = ("title", "description")


class ProgramsAdminGroup(ModelAdminGroup):
    menu_icon = "folder-inverse"
    menu_label = "Programs"
    menu_order = 700
    items = (WebinarAdmin,)


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
