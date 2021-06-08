from .models import Attendance, AttendanceIssue
from django.views.generic import TemplateView
from django.shortcuts import redirect
from wagtail.contrib.modeladmin.views import InspectView



class TodayAttendance(TemplateView):
    """Handle Requests for attendance"""

    template_name = "home/today_attendance.html"

    def post(self, request, **args):
        try:
            if request.user and (not request.user.is_attended_today):
                Attendance.objects.create(
                    member=request.user,
                    issue_date=AttendanceIssue.objects.get(is_open=True),
                    status=True,
                )
        except Exception:
            pass
        return redirect("/admin")


class AttendanceIssueInspect(InspectView):
    def get_context_data(self, **kwargs):
        context = {
            'absentee_list' : self.model.get_absentee_list(self.instance)
        }
        context.update(kwargs)
        return super().get_context_data(**context)