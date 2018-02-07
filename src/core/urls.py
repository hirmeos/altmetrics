from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        '',
        include('importer.urls')
    ),
    path(
        '',
        include('processor.urls')
    ),
    path(
        '',
        include('django.contrib.auth.urls')
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        's3direct/',
        include('s3direct.urls')
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
