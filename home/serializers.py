from rest_framework import serializers
from wagtail.api.v2.serializers import BaseSerializer, DetailUrlField
from .models import Project, ProjectSection, ResearchPaper, User
# from .api import api_router

class ProjectSerializer(BaseSerializer):
    sections = serializers.StringRelatedField(many=True)
    detail_url = DetailUrlField(read_only=True)
    meta_fields =[]

    class Meta:
        model = Project
        fields ="__all__"
        
 

class ProjectSectionSerializer(BaseSerializer):  
    detail_url = DetailUrlField(read_only=True)
    meta_fields =[]

    class Meta:
        model = ProjectSection
        fields = ['id','name', 'slug','detail_url']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name', 'fb_profile_link']


class ResearchPaperSerializer(BaseSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model =  ResearchPaper
        fields = "__all__"