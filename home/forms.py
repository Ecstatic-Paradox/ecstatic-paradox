from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from .models import Department, User


class CustomUserEditForm(UserEditForm):
    country = forms.CharField(required=True, label=_("Country"))
    address = forms.CharField(required=False, label=_("Address"))
    contact = forms.CharField(required=False, label=_("Contact"))
    user_department = forms.ModelChoiceField(
        queryset=Department.objects, required=True, label=_("Department")
    )
    institution = forms.CharField(required=False, label=_("Institution"))
    fb_profile_link = forms.CharField(required=False, label=_("Facebook Profile Link"))
    bio = forms.Textarea()


class CustomUserCreationForm(UserCreationForm):
    country = forms.CharField(required=True, label=_("Country"))
    address = forms.CharField(required=False, label=_("Address"))
    contact = forms.CharField(required=False, label=_("Contact"))
    user_department = forms.ModelChoiceField(
        queryset=Department.objects, required=True, label=_("Department")
    )
    institution = forms.CharField(required=False, label=_("Institution"))
    fb_profile_link = forms.CharField(required=False, label=_("Facebook Profile Link"))
    bio = forms.Textarea()
