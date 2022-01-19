from wagtail.core import hooks
from django.urls import path

from home.views import (
    FillAttendance,
    AttendanceIssueInspect,
    MarkMemberOnLeaveView,
    AddMemberasAbsent,
    ApplyForLeaveView,
    MembersListView,
    MemberInspectView

)
hooks.register(
    "register_admin_urls",
    lambda: [
        path('members', MembersListView.as_view(), name='members' ),
        path('members/<int:pk>', MemberInspectView.as_view(), name='member-profile' ),
        path("fill-attendance/", FillAttendance.as_view(), name="fill-attendance"),
        path(
            "mark-member-on-leave/",
            MarkMemberOnLeaveView.as_view(),
            name="mark-member-on-leave",
        ),
        path(

             # this is for HR to add the absent member on the list
            "add-member-as-absent/", AddMemberasAbsent.as_view(), name="add-member-absent"
        ), 
        path("apply-for-leave/", ApplyForLeaveView.as_view(), name="apply-for-leave" ), #link to apply for leave
        
    ],
)