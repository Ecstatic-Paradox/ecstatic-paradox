from django.db.models import fields
from django.db.models.query_utils import select_related_descend
from rest_framework import serializers
from wagtail.api.v2.serializers import BaseSerializer, DetailUrlField, PageSerializer
from .models import (
    BlogPostPage,
    Project,
    ProjectSection,
    ResearchPaper,
    User,
    Collaborators,
)
from wagtail.users.models import UserProfile
from django.utils.text import Truncator

# from .api import api_router


class AuthorSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["first_name", "last_name", "fb_profile_link","avatar"]

    def get_avatar(self, instance):
        if instance.wagtail_userprofile.avatar:
            return instance.wagtail_userprofile.avatar
        return None

class ProjectSerializer(BaseSerializer):
    sections = serializers.StringRelatedField(many=True)
    detail_url = DetailUrlField(read_only=True)
    content = serializers.SerializerMethodField()
    title = serializers.CharField()
    # thumbnail = serializers.ImageField()
    description = serializers.CharField()
    members = AuthorSerializer(many=True, read_only=True)
    meta_fields = []
    child_serializer_classes = {}  # added just to make it work, idk why it works

    class Meta:
        model = Project
        fields = "__all__"
        # extra_kwargs = {'detail_url': {'lookup_field': 'slug'}}

    def get_content(self, instance):
        ret = []
        if instance.content:
            for i in instance.content:
                ret.append({"type": i.block_type, "value": i.render()})
            return ret
        return None

class ProjectListSerializer(BaseSerializer):
    sections = serializers.StringRelatedField(many=True)
    detail_url = DetailUrlField(read_only=True)
    title = serializers.CharField()
    # thumbnail = serializers.ImageField()
    description = serializers.SerializerMethodField()
    # members = AuthorSerializer(many=True, read_only=True)
    meta_fields = []
    child_serializer_classes = {}  # added just to make it work, idk why it works
    
    class Meta:
        model = Project
        fields = ["title", "detail_url", "slug", "sections", "thumbnail", "description"]

    def get_description(self, instance):
        return Truncator(instance.description).chars(40)


class ProjectSectionSerializer(BaseSerializer):
    # detail_url = DetailUrlField(read_only=True)
    # detail_url = serializers.HyperlinkedRelatedField(
    #     lookup_field = 'slug', view_name='projectsectionapiviewset', read_only=True
    # )
    meta_fields = []
    project_set = ProjectListSerializer(many=True)

    class Meta:
        model = ProjectSection
        fields = ["id", "name", "slug", "detail_url", "project_set"]
        # extra_kwargs = {'detail_url': {'lookup_field': 'slug'}}


class ResearchPaperSerializer(BaseSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    content = serializers.SerializerMethodField()
    class Meta:
        model = ResearchPaper
        fields = "__all__"
    
    def get_content(self, instance):
        ret = []
        if instance.content:
            for i in instance.content:
                ret.append({"type": i.block_type, "value": i.render()})
            return ret
        return None



class CollaboratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborators
        fields = "__all__"


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["avatar"]


class CoreMemberSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "designation",
            "user_department",
            "fb_profile_link",
            "avatar",
        ]

    def get_avatar(self, instance):
        if instance.wagtail_userprofile.avatar:
            return instance.wagtail_userprofile.avatar.url
        return None


class BlogPostPageSerializer(PageSerializer):
    content = serializers.SerializerMethodField()
    detail_url = DetailUrlField(read_only=True)
    # thumbnail = serializers.ImageField()
    owner = AuthorSerializer(read_only=True)
    meta_fields = ["title","slug","detail_url","date_created", "owner"]

    child_serializer_classes = {}  # added just to make it work, idk why it works

    class Meta:
        model = BlogPostPage
        fields = [
            "title",
            "seo_title",
            "date_created",
            "slug",
            "detail_url",
            "view_count",
            "date_created",
            "content",
            "tags",
            "thumbnail",
            "is_pinned",
            "owner",

        ]
        # fields = "__all__"
        extra_kwargs = {"detail_url": {"lookup_field": "slug"}}

    def get_content(self, instance):
        ret = []
        if instance.content:
            for i in instance.content:
                ret.append({"type": i.block_type, "value": i.render()})
            return ret
        return None
