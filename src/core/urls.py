from django.contrib import admin
from django.urls import path, include

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
]
