from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from wagtail.api.v2.views import BaseAPIViewSet
from rest_framework import serializers
from .models import (
    Article,
    Webinar,
    Symposium,
    Course,
    ResearchPaper,
    Project,
    ProjectSection

)
from .serializers import ProjectSerializer

api_router = WagtailAPIRouter("wagtailapi")


class ArticleAPIViewSet(BaseAPIViewSet):
    model = Article

    def get_queryset(self):
        return self.model.objects.filter(live=True).order_by("-id")


class WebinarAPIViewSet(BaseAPIViewSet):
    model = Webinar

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")


class SymposiumAPIViewSet(BaseAPIViewSet):
    model = Symposium

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

class CourseAPIViewSet(BaseAPIViewSet):
    model = Course

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

class ResearchPaperAPIViewSet(BaseAPIViewSet):
    model = ResearchPaper

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

class ProjectAPIViewSet(BaseAPIViewSet):
    model = Project
    base_serializer_class = ProjectSerializer
    # meta_fields = ['detail_url','type']
    listing_default_fields  = ['id','sections','detail_url']
    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

class ProjectSectionAPIViewSet(BaseAPIViewSet):
    model = ProjectSection
    def get_queryset(self):
        return self.model.objects.all()

# api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
api_router.register_endpoint("articles", ArticleAPIViewSet)
api_router.register_endpoint("webinars", WebinarAPIViewSet)
api_router.register_endpoint("symposiums", SymposiumAPIViewSet)
api_router.register_endpoint("courses", CourseAPIViewSet)
api_router.register_endpoint("researchpapers", ResearchPaperAPIViewSet)
api_router.register_endpoint("projects", ProjectAPIViewSet)
api_router.register_endpoint("projects/sections", ProjectSectionAPIViewSet)
