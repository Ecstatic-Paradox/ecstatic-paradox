from operator import imod
from django.conf import settings
from django.urls import include, path 
from django.contrib import admin
from django.views.generic import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from home.api import api_router
from home.views import CustomLoginView, GiveAbsentReason

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/login/", CustomLoginView.as_view(), name="custom_login"),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/", api_router.urls),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path(
        # this is to ask members reason why they were absent.
        "give-absent-reason/",
        GiveAbsentReason.as_view(),
        name="give-absent-reason",
    ),
    path(
        "captcha/", include("captcha.urls")
    ),  # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # path("", include(wagtail_urls)),
    path("", RedirectView.as_view(url="/admin")),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
