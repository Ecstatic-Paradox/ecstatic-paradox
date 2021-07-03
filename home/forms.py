from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, AskForLeaveMember

from wagtail.admin.widgets.datetime import AdminDateInput

class CustomProfileSettingsForm(forms.ModelForm):
    country = forms.CharField(required=True, label=_("Country"))

    class Meta:
        model = User
        fields = (
            "country",
            "date_of_birth",
            "address",
            "contact",
            "user_department",
            "institution",
            "bio",
            "fb_profile_link",
        )


class CustomUserEditForm(UserEditForm):
    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}



class AskForLeaveForm(forms.ModelForm):
    # To show date picker 
    leave_start_date = forms.DateField(widget=AdminDateInput)
    
    class Meta:
        model = AskForLeaveMember
        fields = ['remarks', 'leave_start_date', 'leave_end_date']

        # This is also to show date picker. Both work fine. :) 
        widgets = {"leave_end_date": forms.DateInput(attrs={"type": "date"})}

