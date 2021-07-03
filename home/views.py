from django import forms
from django.views.generic.base import View
from .models import Attendance, AttendanceIssue, User, Absentee, AskForLeaveMember
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from wagtail.contrib.modeladmin.views import InspectView
from .forms import AskForLeaveForm


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
        context = {"absentee_list": self.model.get_absentee_list(self.instance)}
        context.update(kwargs)
        return super().get_context_data(**context)


class MarkMemberOnLeaveView(View):
    """Handles admin/mark-member-on-leave/ from attandanceinspect view"""

    http_method_names = [
        "post",
    ]
    permission_required = ("manage_attendance",)

    def post(self, request, *args, **kwargs):
        member_obj = User.objects.get(id=request.POST["member_id"])
        attendance_issue = AttendanceIssue.objects.get(
            id=request.POST["attendance_issue"]
        )
        attendance = Attendance.objects.create(
            issue_date=attendance_issue,
            member=member_obj,
            status=False,
            remarks=request.POST["remarks"],
        )
        attendance.save()
        return redirect(f"/admin/home/attendanceissue/inspect/{ attendance_issue.id }/")


class AskMemberReasonView(View):
    """Handles admin/ask-member-reason/ from attandanceinspect view"""

    http_method_names = ["post"]
    permission_required = ("manage_attendance",)

    def post(self, request, *args, **kwargs):
        member_obj = User.objects.get(id=request.POST["member_id"])
        attendance_issue = AttendanceIssue.objects.get(
            id=request.POST["attendance_issue"]
        )
        absentee_obj = Absentee.objects.create(
            issue_date=attendance_issue, member=member_obj
        )
        absentee_obj.save()

        return redirect(f"/admin/home/attendanceissue/inspect/{ attendance_issue.id }/")


class AskForLeaveView(View):
    form_class = AskForLeaveForm
    permission_required = "manage_attendance"
    template_name = "wagtailadmin/generic/create.html"
    page_title = "Ask For Leave Form"
    header_icon = "date"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {"form": self.form_class, "view": self}
        )

    def post(self, request):
        form_data = self.form_class(request.POST)
        if form_data.is_valid():
            obj = AskForLeaveMember.objects.create(
                member=request.user,
                remarks = form_data.cleaned_data["remarks"],
                leave_start_date = form_data.cleaned_data["leave_start_date"],
                leave_end_date = form_data.cleaned_data["leave_end_date"],
            )
            obj.save()
        return redirect("/admin")
