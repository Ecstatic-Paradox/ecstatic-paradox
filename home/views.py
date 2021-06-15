from django.views.generic.base import View
from .models import Attendance, AttendanceIssue, User, Absentee
from django.views.generic import TemplateView
from django.shortcuts import redirect
from wagtail.contrib.modeladmin.views import InspectView
# from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin


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



class MarkMemberOnLeaveView(View):
    http_method_names = ['post',]
    permission_required = ('manage_attendance',)

    def post(self, request, *args, **kwargs):
        # print(f'\n\n\n {request.POST} \n\n\n')
        member_obj = User.objects.get(id=request.POST['member_id'])
        attendance_issue = AttendanceIssue.objects.get(id=request.POST['attendance_issue'])
        attendance = Attendance.objects.create(
            issue_date= attendance_issue,
            member=member_obj,
            status=False,
            remarks=request.POST['remarks']
        )
        attendance.save()
        return redirect(f'/admin/home/attendanceissue/inspect/{ attendance_issue.id }/')

class AskMemberReasonView(View):
    http_method_names = ['post']
    permission_required = ('manage_attendance',)

    def post(self, request, *args, **kwargs):
        member_obj = User.objects.get(id=request.POST['member_id'])
        attendance_issue = AttendanceIssue.objects.get(id=request.POST['attendance_issue'])
        absentee_obj = Absentee.objects.create(
            issue_date=attendance_issue,
            member=member_obj
        )
        absentee_obj.save()

        return redirect(f'/admin/home/attendanceissue/inspect/{ attendance_issue.id }/')

