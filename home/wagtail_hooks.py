from django.urls import reverse
from django.urls import path, reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Attendance


@hooks.register("construct_main_menu")
def main_menu_edit(request, menu_items):
    """Remove Pages option from dashboard menu"""
    menu_items[:] = [i for i in menu_items if (i.label not in ["Pages"])]
    pass


