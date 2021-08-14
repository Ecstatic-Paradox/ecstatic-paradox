from django.http.response import Http404
from django.views.generic.base import View
from .models import Attendance, AttendanceIssue, User, Absentee, AskForLeaveMember
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from wagtail.contrib.modeladmin.views import InspectView
from .forms import AskForLeaveForm, GiveAbsentReasonForm
from wagtail.admin.views.account import LoginView

class CustomLoginView(LoginView):
    """ Handles Login, Especially redirects user to Form if they have unspecified leave. """ 
    template_name = "home/ep_login.html"
    def get_success_url(self):

        # TODO : check if user was absent then  lead them to fill up form .. else super().get_success_url()
        if self.request.user.has_unrecorded_leave:
            return "/give-absent-reason/"
        return super().get_success_url()


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

class GiveAbsentReason(View):
    template_name = "home/give-absent-reason.html"
    form_class = GiveAbsentReasonForm

    
    def get(self, request, *args, **kwargs):
        if self.request.user:

            unfilled_instance = Absentee.objects.filter(member=self.request.user).filter(remarks="").first()
            
            form = GiveAbsentReasonForm(instance=unfilled_instance)

            return render(
                request, self.template_name, {"form": form, "view": self}
            )

        return redirect('/admin')
    
    def post(self, request, *args, **kwargs):
            print(request.POST)
        # try: 
            issue_date_id = int(request.POST["issue_date"])
        # except:
            # raise Http404
            return redirect('/admin')
        