from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.menu import MenuItem

from django.urls import reverse
from django.http.response import HttpResponseRedirect

from home.models import HomePage

@hooks.register("construct_main_menu")
def main_menu_edit(request, menu_items):
    """Remove Pages, Images, Documents, Reports option from dashboard menu for non superusers"""
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
