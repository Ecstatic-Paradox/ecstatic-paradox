from wagtail.core import hooks
from home.models import Notification
from django.db.models import Q, F
from django.template.loader import render_to_string
import datetime


# Add notifications Section in Dashboard Home
class NotificationPanel:

    order = 50

    def __init__(self, request):
        self.request = request

    def render(self):
        unexpired = Notification.objects.filter(has_expired=False).filter(
            Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date=None)
        )

        # expired_bool = Notification.objects.filter(has_expired=True)
        # expired = (
        #     Notification.objects.filter(expiry_date__lte=datetime.datetime.now())
        #     .union(expired_bool)
        #     .order_by("-date_added")
        # )

        if unexpired.count() == 0 and expired.count() == 0:
            return render_to_string(
                "home/home_notifications.html",
                {"notifications": False},
                request=self.request,
            )

        return render_to_string(
            "wagtailadmin/home/dashboard_notice.html",
            {
                "notifications": True,
                "notices": unexpired,
            },
            request=self.request,
        )


class AttendanceButtonPanel:
    order = 49

    def __init__(self, request):
        self.request = request

    def render(self):
        issue = self.request.user.get_unattended_issue()

        if not issue:

            return render_to_string(
                "wagtailadmin/home/attendance_issue.html",
                {
                    "is_unattended": False,
                },
                request=self.request,
            )

        return render_to_string(
            "wagtailadmin/home/attendance_issue.html",
            {"is_unattended": True, "issue": issue},
            request=self.request,
        )


class AbsentDatesPanel:
    order = 51

    def __init__(self, request):
        self.request = request

    def render(self):
        records = self.request.user.get_absent_record()

        if not records:

            return render_to_string(
                "wagtailadmin/home/absent_dates.html",
                {
                    "has_records": False,
                },
                request=self.request,
            )

        return render_to_string(
            "wagtailadmin/home/absent_dates.html",
            {"has_records": True, "records": records},
            request=self.request,
        )


@hooks.register("construct_homepage_panels")
def add_notifications_panel(request, panels):
    panels.pop(0)  # Remove the site_summary ie. Image 2, Docs 4 blah blah
    panels.append(NotificationPanel(request))
    panels.append(AttendanceButtonPanel(request))
    panels.append(AbsentDatesPanel(request))
    
