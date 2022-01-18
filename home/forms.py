from django import forms
from django.db import models
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, AskForLeaveMember, Absentee

from wagtail.admin.widgets.datetime import AdminDateInput

from captcha.fields import CaptchaField


class CustomProfileSettingsForm(forms.ModelForm):
    country = forms.CharField(required=True, label=_("Country"))

    class Meta:
        model = User
        fields = (
            "country",
            "date_of_birth",
            "address",
            "contact",
            "gender",
            "user_department",
            "institution",
            "bio",
            "linkedIn_profile",
            "personal_website",
            "designation",
            # "is_core_member"  #don't add it here, else users will be able to change themselves into core member

        )
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class CustomUserEditForm(UserEditForm):
    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}

class FillAttendanceForm(forms.Form):
    """ Attendance Form """
    captacha = CaptchaField()

class ApplyForLeaveForm(forms.ModelForm):
    # To show date picker 
    leave_start_date = forms.DateField(widget=AdminDateInput)
    
    class Meta:
        model = AskForLeaveMember
        fields = ['remarks', 'leave_start_date', 'leave_end_date']

        # This is also to show date picker. Both work fine. :) 
        widgets = {"leave_end_date": forms.DateInput(attrs={"type": "date"})}

class GiveAbsentReasonForm(forms.ModelForm):
    class Meta:
        model = Absentee
        fields = ['remarks','issue_date']
        widgets = {
            'issue_date': forms.HiddenInput(attrs={"readonly":"" })
            }
    def __init__(self,  *args, **kwargs):
        super(GiveAbsentReasonForm, self).__init__()

        # Auto fill the value for issue_date hidden 
        self.fields['issue_date'].widget.attrs["value"] = kwargs['instance'].issue_date.id           