from django.conf import settings
from django.conf.urls.static import static
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
    path(
        'api/',
        include('api.urls')
    )
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if not settings.DEBUG:
    urlpatterns.append(
        path(
            '',
            include('static_handler.urls')
        )
    )
