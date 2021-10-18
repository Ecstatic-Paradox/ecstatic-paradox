from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotFound
from django.utils import safestring
from django.views.generic.base import View
from django.views.generic import TemplateView, DetailView, ListView

from .models import Attendance, AttendanceIssue, User, Absentee, AskForLeaveMember
from django.shortcuts import redirect, render
from wagtail.contrib.modeladmin.views import InspectView
from .forms import ApplyForLeaveForm, GiveAbsentReasonForm, FillAttendanceForm
from wagtail.admin.views.account import LoginView


class CustomLoginView(LoginView):
    """Handles Login, Especially redirects user to Form if they have unspecified leave."""

    template_name = "home/ep_login.html"

    def get_success_url(self):

        # checks if user has unrecordeed leave and removes all permission if True
        if self.request.user.has_unrecorded_leave:
            return "/give-absent-reason/"
        return super().get_success_url()


class FillAttendance(TemplateView):
    """Handle Requests for attendance"""

    template_name = "home/fill_attendance.html"
    form_class = FillAttendanceForm
    
    def get_context_data(self, **kwargs):
        context = {"form": self.form_class}
        context.update(kwargs)
        return super().get_context_data(**context)

    def post(self, request, **args):
        form = FillAttendanceForm(request.POST)
        if form.is_valid():
            try:
                if request.user and (not bool(request.user.get_unattended_issue())):
                    print(f"\n\n\n {request.user} \n\n\n {AttendanceIssue.objects.get(is_open=True)} \n\n\n ")
                    attendance = Attendance.objects.create(
                        member=request.user,
                        issue_date=AttendanceIssue.objects.get(is_open=True),
                        status=True,
                    )
                    attendance.save()
            except Exception as e:
                print("\n\n {} \n\n ".format(e))
                return HttpResponseNotFound()
            return redirect("/admin")
        
        else:
            return HttpResponseBadRequest()


class AttendanceIssueInspect(InspectView):
    """Adds absentee information in Attendance Inspect View"""

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
        try:
            member_obj = User.objects.get(id=request.POST["member_id"])
            attendance_issue = AttendanceIssue.objects.get(
                id=request.POST["attendance_issue"]
            )
        except User.DoesNotExist or AttendanceIssue.DoesNotExist:
            return HttpResponseNotFound()

        attendance = Attendance.objects.create(
            issue_date=attendance_issue,
            member=member_obj,
            status=False,
            remarks=request.POST["remarks"],
        )
        attendance.save()
        return redirect(f"/admin/home/attendanceissue/inspect/{ attendance_issue.id }/")


class AddMemberasAbsent(View):
    """Handles admin/ask-member-reason/ from attandanceinspect view"""

    http_method_names = ["post"]
    permission_required = ("manage_attendance",)

    def post(self, request, *args, **kwargs):
        try:
            member_obj = User.objects.get(id=request.POST["member_id"])
            attendance_issue = AttendanceIssue.objects.get(
                id=request.POST["attendance_issue"]
            )
        except User.DoesNotExist or AttendanceIssue.DoesNotExist:
            return HttpResponseNotFound()
        absentee_obj = Absentee.objects.create(
            issue_date=attendance_issue, member=member_obj
        )
        absentee_obj.save()

        return redirect(f"/admin/home/attendanceissue/inspect/{ attendance_issue.id }/")


class ApplyForLeaveView(View):
    form_class = ApplyForLeaveForm
    permission_required = "manage_attendance"
    template_name = "wagtailadmin/generic/create.html"
    page_title = "Apply For Leave Form"
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
                remarks=form_data.cleaned_data["remarks"],
                leave_start_date=form_data.cleaned_data["leave_start_date"],
                leave_end_date=form_data.cleaned_data["leave_end_date"],
            )
            obj.save()
        return redirect("/admin")


class GiveAbsentReason(View):
    template_name = "home/give-absent-reason.html"
    form_class = GiveAbsentReasonForm

    def get(self, request, *args, **kwargs):
        if self.request.user:
            try:
                unfilled_user_instance = Absentee.objects.filter(
                    member=self.request.user
                )

                unfilled_remarks_instance = unfilled_user_instance.filter(remarks=None)
                unfilled_instance = unfilled_remarks_instance.first()

                if unfilled_instance == None:
                    raise Absentee.DoesNotExist

            except Absentee.DoesNotExist:
                return redirect("/admin")

            form = GiveAbsentReasonForm(instance=unfilled_instance)

            return render(
                request,
                self.template_name,
                {
                    "page_title": "Give Reason for absent on "
                    + str(unfilled_instance.issue_date.date),
                    "form": form,
                    "view": self,
                },
            )

        return redirect("/admin")

    def post(self, request, *args, **kwargs):
        if self.request.user:
            try:
                issue_date_id = int(request.POST["issue_date"])
                remarks = safestring.SafeString(request.POST["remarks"])

                issue_date_instance = AttendanceIssue.objects.get(id=issue_date_id)
                absentee_instance = Absentee.objects.get(
                    issue_date=issue_date_instance,
                    member=self.request.user,
                    remarks=None,
                )
            except:
                return HttpResponseBadRequest()

            absentee_instance.remarks = remarks
            absentee_instance.save()

        return redirect("/admin")


class MembersListView(ListView):
    template_name = "home/members_list.html"
    context_object_name = "members"
    model = User

    


class MemberInspectView(DetailView):

    template_name= "home/member_profile.html"
    context_object_name = "member"
    model = User

