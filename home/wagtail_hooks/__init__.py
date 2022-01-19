from wagtail.core import hooks
from django.utils.html import format_html
from django.templatetags.static import static
from .custom_urls import *
from .edit_menu import *
from .homepage_panels import *
from .modeladmins import *

@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/colors.css"))

# Additional Custom Css
@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/ep_css.css"))

from home.models import BlogPostPage
@hooks.register("before_serve_page")
def increment_view_count(page, request, serve_args, serve_kwargs):
    if page.specific_class == BlogPostPage:
        BlogPostPage.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)

# Customize account settings, Add My profile section in Account Settings Panel
from home.forms import CustomProfileSettingsForm
from wagtail.admin.views.account import BaseSettingsPanel
@hooks.register("register_account_settings_panel")
class CustomSettingsPanel(BaseSettingsPanel):
    name = "profile"
    title = "My profile"
    order = 290
    form_class = CustomProfileSettingsForm
    form_object = "user"

