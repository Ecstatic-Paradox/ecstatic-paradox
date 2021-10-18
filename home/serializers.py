from rest_framework import serializers
from wagtail.api.v2.serializers import BaseSerializer, DetailUrlField
from .models import Project, ProjectSection


class ProjectSerializer(BaseSerializer):
    sections = serializers.StringRelatedField(many=True)
    detail_url = DetailUrlField(read_only=True)


class ProjectSectionSerializer(BaseSerializer):
    pass