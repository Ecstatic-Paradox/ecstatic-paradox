from .models import Attendance, AttendanceIssue
from django.views.generic import TemplateView
import datetime
from django.shortcuts import redirect

class TodayAttendance(TemplateView):
    """Handle Requests for attendance"""
    template_name = "today_attendance.html"

    def post(self, request, **args):
        try:
            if request.user and (not request.user.profile.is_attended_today):
                Attendance.objects.create(
                member=request.user, issue_date=AttendanceIssue.objects.get(date=datetime.date.today()), status=True,
            )
        except Exception:
            pass
        return redirect("/admin")