from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.api.v2.views import BaseAPIViewSet

from .models import (
    Article,
    Webinar,
    Symposium,
    Course,
    ResearchPaper,
    Project,

)

api_router = WagtailAPIRouter("wagtailapi")


class ArticleAPIViewSet(BaseAPIViewSet):
    model = Article

    def get_queryset(self):
        return self.model.objects.filter(live=True).order_by("-date_published")


class WebinarAPIViewSet(BaseAPIViewSet):
    model = Webinar

    def get_queryset(self):
        return self.model.objects.all().order_by("-date")


class SymposiumAPIViewSet(BaseAPIViewSet):
    model = Symposium

    def get_queryset(self):
        return self.model.objects.all().order_by("-date")

class CourseAPIViewSet(BaseAPIViewSet):
    model = Course

    def get_queryset(self):
        return self.model.objects.all().order_by("-date")

class ResearchPaperAPIViewSet(BaseAPIViewSet):
    model = ResearchPaper

    def get_queryset(self):
        return self.model.objects.all().order_by("-date_published")

class ProjectAPIViewSet(BaseAPIViewSet):
    model = Project

    def get_queryset(self):
        return self.model.objects.all().order_by("-start_date")


# api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
api_router.register_endpoint("articles", ArticleAPIViewSet)
api_router.register_endpoint("webinars", WebinarAPIViewSet)
api_router.register_endpoint("symposiums", SymposiumAPIViewSet)
api_router.register_endpoint("courses", CourseAPIViewSet)
api_router.register_endpoint("researchpapers", ResearchPaperAPIViewSet)
api_router.register_endpoint("projects", ProjectAPIViewSet)
