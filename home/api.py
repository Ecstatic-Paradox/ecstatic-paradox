from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.api.v2.views import BaseAPIViewSet

from .models import Article

api_router = WagtailAPIRouter("wagtailapi")


class ArticleAPIViewSet(BaseAPIViewSet):
    model = Article

    def get_queryset(self):
        return self.model.objects.filter(live=True).order_by("-date_published")


# api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
api_router.register_endpoint("articles", ArticleAPIViewSet)
