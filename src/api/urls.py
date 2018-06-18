from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from api.views import (
    schema_view,
    AltmetricViewSet,
    DoiUploadViewSet,
    EventViewSet,
    ScrapeViewSet,
    UriViewSet,
    UrlViewSet,
)


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'uri', UriViewSet)
router.register(r'altmetrics', AltmetricViewSet)
router.register(r'uriupload', DoiUploadViewSet)
router.register(r'event', EventViewSet)
router.register(r'scrape', ScrapeViewSet)
router.register(r'url', UrlViewSet)

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
    path(
        '',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    path(
        'docs',
        schema_view
    ),
]
