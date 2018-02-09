from django.urls import re_path, include
from django.conf import settings

from .views import StaticFileServeView


urlpatterns = [
    re_path(
        r'^static/(?P<path>.*)$',
        StaticFileServeView.as_view()
    ),
]

