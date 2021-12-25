from django.views import generic
from django.urls import reverse
from rest_framework.response import Response
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from django.shortcuts import get_object_or_404
from django.urls import path
from wagtail.api.v2.views import BaseAPIViewSet, PagesAPIViewSet
from rest_framework import serializers, viewsets
from django.utils.text import Truncator
from django.db.models import F

from .models import (
    BlogPostPage,
    Gallery,
    User,
    Article,
    Collaborators,
    Webinar,
    Symposium,
    Course,
    ResearchPaper,
    Project,
    ProjectSection,
)
from .serializers import (
    BlogPostPageSerializer,
    CollaboratorsSerializer,
    CoreMemberSerializer,
    ProjectSerializer,
    ProjectListSerializer,
    ProjectSectionSerializer,
    ResearchPaperSerializer,
)

api_router = WagtailAPIRouter("wagtailapi")


def slug_url_pattern(cls):
    """URL patterns for viewsets which needs slug url"""
    return [
        path("", cls.as_view({"get": "listing_view"}), name="listing"),
        path("<slug:slug>/", cls.as_view({"get": "detail_view"}), name="detail"),
        path("find/", cls.as_view({"get": "find_view"}), name="find"),
    ]


"""" 
 Note: Usage of
    1. meta_fields is to include fields in meta in detail view (/api/<endpoint>/<id>)
    2. body_fields is to include fields in body in detail view
    3. listing default fields inlcudes in list view 
"""



class EPBaseAPIViewSet(BaseAPIViewSet):
    def detail_view(self, request, pk=None, slug=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @classmethod
    def get_urlpatterns(cls):

        """URL patterns for viewsets which needs slug url"""

        if cls.lookup_field == "slug":
            return [
                path("", cls.as_view({"get": "listing_view"}), name="listing"),
                path(
                    "<slug:slug>/", cls.as_view({"get": "detail_view"}), name="detail"
                ),
                path("find/", cls.as_view({"get": "find_view"}), name="find"),
            ]
        else:
            return [
                path("", cls.as_view({"get": "listing_view"}), name="listing"),
                path(
                    "<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"
                ),
                path("find/", cls.as_view({"get": "find_view"}), name="find"),
            ]
            # return super().get_urlpatterns()


    @classmethod
    def get_object_detail_urlpath(cls, model, pk, namespace=""):
        if namespace:
            url_name = namespace + ":detail"
        else:
            url_name = "detail"

        if cls.lookup_field == 'slug':
            obj = model.objects.get(pk=pk)
            return reverse(url_name, args=(obj.slug,))
        else:
            return reverse(url_name, args=(pk,))




# Add fields in Viewsets and also in api_fields in model


class ArticleAPIViewSet(EPBaseAPIViewSet):
    model = Article
    lookup_field = 'slug'
    meta_fields = ['title','detail_url', ]
    body_fields = ['id','slug','thumbnail','pdf_file','date_published','author']
    listing_default_fields= ['id','slug',"title","date_published",'thumbnail', "detail_url",'author']
    def get_queryset(self):
        return self.model.objects.filter(live=True).order_by("-id")


class WebinarAPIViewSet(BaseAPIViewSet):
    meta_fields = ['id','title','detail_url', ]
    
    body_fields = ['id', 'date', 'thumbnail','youtube_link', 'registration_form', 'description']

    listing_default_fields = ['title', 'detail_url', 'id', 'date', 'thumbnail']
    model = Webinar

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")


class SymposiumAPIViewSet(BaseAPIViewSet):
    meta_fields = ['id','title','detail_url', ]
    
    body_fields = ['id', 'date', 'thumbnail','youtube_link', 'registration_form', 'description']

    listing_default_fields = ['title', 'detail_url', 'id', 'date', 'thumbnail']

    model = Symposium

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")


class CourseAPIViewSet(BaseAPIViewSet):
    meta_fields = ['id','title','detail_url', ]
    
    body_fields = ['id', 'date', 'thumbnail','youtube_link', 'registration_form', 'description']

    listing_default_fields = ['title', 'detail_url', 'id', 'date', 'thumbnail']

    model = Course

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")


class ResearchPaperAPIViewSet(BaseAPIViewSet):
    model = ResearchPaper
    base_serializer_class = ResearchPaperSerializer

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")


class ProjectAPIViewSet(EPBaseAPIViewSet):
    model = Project
    base_serializer_class = ProjectSerializer
    meta_fields = ['sections'] #detail_url
    body_fields = ["id","slug", "detail_url"]
    listing_default_fields  = ['id','title','thumbnail','slug']
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def listing_view(self, request):
        response = super().listing_view(request)
        sections_queryset = ProjectSection.objects.all()
        sections_serializer = ProjectSectionSerializer(
            sections_queryset, many=True, context=self.get_serializer_context()
        )
        response.data["meta"]["sections"] = sections_serializer.data
        # try:
        #     response.data["description"] = Truncator(response.data["description"]).words(2)
        # except Exception:
        #     pass

        return response

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")


class ProjectSectionAPIViewSet(EPBaseAPIViewSet):
    model = ProjectSection
    base_serializer_class = ProjectSectionSerializer
    serializer_class = ProjectSectionSerializer
    body_fields = ["slug", "detail_url"]
    meta_fields = ["detail_url", "name"]
    listing_default_fields = ["id", "name", "slug"]
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def detail_view(self, request, pk=None, slug=None):
        param = slug

        if pk is not None:
            self.lookup_field = "pk"
            param = pk

        res = super().detail_view(request, param)
        if pk:
            instance = self.model.objects.get(pk=pk)
        elif slug:
            instance = self.model.objects.get(slug=slug)

        projects_queryset = instance.project_set.all()
        projects_serializer = ProjectListSerializer(
            projects_queryset, many=True, context=self.get_serializer_context()
        )

        res.data["items"] = projects_serializer.data

        return res

    def get_queryset(self):
        return self.model.objects.all()




class AboutAPIViewSet(BaseAPIViewSet):
    model = Collaborators

    def collaborators_list(self, req):
        queryset = Collaborators.objects.all()
        serializer = CollaboratorsSerializer(
            queryset, many=True, context=self.get_serializer_context()
        )

        return Response(serializer.data)

    def members_list(self, req):
        queryset = User.objects.all().filter(is_core_member=True)
        serializer = CoreMemberSerializer(
            queryset, many=True, context=self.get_serializer_context()
        )

        return Response(serializer.data)

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path(
                "collaborators/",
                cls.as_view({"get": "collaborators_list"}),
                name="detail",
            ),
            path("coremembers/", cls.as_view({"get": "members_list"}), name="detail"),
        ]


class BlogAPIViewSet(EPBaseAPIViewSet):
    
    model = BlogPostPage
    base_serializer_class = BlogPostPageSerializer
    meta_fields = ['detail_url', 'title', "owner","date_created"]
    listing_default_fields = ["id","title","detail_url", "thumbnail", "owner","date_created"]
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        return self.model.objects.all().order_by("-id")

    def pinnedpost_list(self, request):
        queryset = self.model.objects.filter(is_pinned=True)
        self.check_query_parameters(queryset)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = self.base_serializer_class(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def popularpost_list(self, request):
        queryset = self.model.objects.all().order_by("-view_count")
        if queryset.count() > 4:
            queryset = queryset[:4]
        self.check_query_parameters(queryset)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = BlogPostPageSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)
    
    def detail_view(self, request, pk=None, slug=None):
        if slug:
            pk = self.model.objects.get(slug=slug).id
        self.model.objects.filter(id=pk).update(view_count=F('view_count')+1)
        return super().detail_view(request, pk)
    
    @classmethod
    def get_urlpatterns(cls):
        return [
                path("pinned/", cls.as_view({"get": "pinnedpost_list"}), name="pinned_posts",),
                path("popular/", cls.as_view({"get": "popularpost_list"}), name="popular_posts",),
        ] +super().get_urlpatterns() 
    

class GalleryAPIViewSet(BaseAPIViewSet):
    model = Gallery
    body_fields = ["thumbnail"]
    listing_default_fields = ["thumbnail"]

#api_router.register_endpoint("pages", PagesAPIViewSet)
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
api_router.register_endpoint("blogs", BlogAPIViewSet)
api_router.register_endpoint("gallery", GalleryAPIViewSet)
