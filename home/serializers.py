from django.db.models import fields
from rest_framework import serializers
from wagtail.api.v2.serializers import BaseSerializer, DetailUrlField
from .models import Project, ProjectSection, ResearchPaper, User, Collaborators
from  wagtail.users.models import UserProfile
# from .api import api_router

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'fb_profile_link']

class ProjectSerializer(BaseSerializer):
    sections = serializers.StringRelatedField(many=True)
    detail_url = DetailUrlField(read_only=True)
    title = serializers.CharField()
    thumbnail = serializers.ImageField()
    description = serializers.CharField()
    members = AuthorSerializer(many=True, read_only=True)
    meta_fields =[]

    class Meta:
        model = Project
        fields ="__all__"

class ProjectListSerializer(BaseSerializer):
    sections = serializers.StringRelatedField(many=True)
    detail_url = DetailUrlField(read_only=True)
    title = serializers.CharField()
    thumbnail = serializers.ImageField()
    description = serializers.CharField()
    # members = AuthorSerializer(many=True, read_only=True)
    meta_fields =[]

    class Meta:
        model = Project
        fields =["title","detail_url","sections","thumbnail","description"]
        

class ProjectSectionSerializer(BaseSerializer):  
    detail_url = DetailUrlField(read_only=True)
    # detail_url = serializers.HyperlinkedRelatedField(
    #     lookup_field = 'slug', view_name='projectsectionapiviewset', read_only=True
    # )
    meta_fields =[]

    class Meta:
        model = ProjectSection
        fields = ['name', 'slug','detail_url']
        extra_kwargs = {'detail_url': {'lookup_field': 'slug'}}



class ResearchPaperSerializer(BaseSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model =  ResearchPaper
        fields = "__all__"


class CollaboratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborators
        fields = '__all__'

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields= ["avatar"]

class CoreMemberSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'designation', 'user_department', 'fb_profile_link', 'avatar']

    def get_avatar(self, instance):
        if instance.wagtail_userprofile.avatar:
            return instance.wagtail_userprofile.avatar.url
        return None