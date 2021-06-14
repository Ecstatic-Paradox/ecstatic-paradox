from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import User


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



# class MarkMemberOnLeaveForm(forms.Form):
