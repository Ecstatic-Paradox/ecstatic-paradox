from django.views import generic
from rest_framework.response import Response
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from django.urls import path
from wagtail.api.v2.views import BaseAPIViewSet
from rest_framework import serializers, viewsets

from .models import (
    User,
    Article,
    Collaborators,
    Webinar,
    Symposium,
    Course,
    ResearchPaper,
    Project,
    ProjectSection

)
from .serializers import CollaboratorsSerializer, CoreMemberSerializer, ProjectSerializer, ProjectSectionSerializer, ResearchPaperSerializer

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
    base_serializer_class = ResearchPaperSerializer

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

class ProjectAPIViewSet(BaseAPIViewSet):
    model = Project
    base_serializer_class = ProjectSerializer
    meta_fields = ['detail_url', 'sections']
    listing_default_fields  = ['id','sections','detail_url','title','thumbnail']

    def listing_view(self, request):
        response = super().listing_view(request)
        sections_queryset = ProjectSection.objects.all()
        sections_serializer = ProjectSectionSerializer(sections_queryset, many=True, context =self.get_serializer_context())
        response.data["meta"]["sections"] = sections_serializer.data

        return response

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

class ProjectSectionAPIViewSet(BaseAPIViewSet):
    model = ProjectSection
    base_serializer_class = ProjectSectionSerializer
    meta_fields = ['detail_url','name']
    listing_default_fields = ['id','detail_url', 'name', 'slug']

    def detail_view(self, request, pk=None, slug=None):
        param = pk

        if slug is not None:
            self.lookup_field = 'slug'
            param = slug

        res = super().detail_view(request, param)
        if pk:
            instance = self.model.objects.get(pk=pk)
        elif slug:
            instance = self.model.objects.get(slug=slug)
        
        
        projects_queryset = instance.project_set.all()
        projects_serializer =  ProjectSerializer(projects_queryset, many=True, context =self.get_serializer_context())

        res.data["items"] = projects_serializer.data

        return res


    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path('', cls.as_view({'get': 'listing_view'}), name='listing'),
            path('<int:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
            path('<slug:slug>/', cls.as_view({'get': 'detail_view'}), name='detail'),
            path('find/', cls.as_view({'get': 'find_view'}), name='find'),
        ]
    
    def get_queryset(self):
        return self.model.objects.all()

class AboutAPIViewSet(BaseAPIViewSet):
    model = Collaborators

    def collaborators_list(self, req):
        queryset = Collaborators.objects.all()
        serializer = CollaboratorsSerializer(queryset, many=True,context =self.get_serializer_context())
        
        return Response(serializer.data)

    def members_list(self, req):
        queryset = User.objects.all().filter(is_core_member=True)
        serializer = CoreMemberSerializer(queryset, many=True,context =self.get_serializer_context())

        return Response(serializer.data)
    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path('collaborators/', cls.as_view({'get': 'collaborators_list'}), name='detail'),
            path('core-members/', cls.as_view({'get': 'members_list'}), name='detail'),
        ]

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
api_router.register_endpoint("about", AboutAPIViewSet)
