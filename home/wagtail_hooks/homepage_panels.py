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
