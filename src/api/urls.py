from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'dois', views.DoiViewSet)
router.register(r'doiuploads', views.DoiUploadViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'scrapes', views.ScrapeViewSet)
router.register(r'urls', views.UrlViewSet)

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
    path(
        '',
        include('rest_framework.urls', namespace='rest_framework')
    )
]
