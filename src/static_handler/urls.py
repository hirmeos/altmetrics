from django.urls import re_path

from .views import StaticFileServeView


urlpatterns = [
    re_path(
        r'^static/(?P<path>.*)$',
        StaticFileServeView.as_view()
    ),
]
