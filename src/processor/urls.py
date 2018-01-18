from django.urls import path

from .views import DoisView


urlpatterns = [
    path(
        'dois',
        DoisView.as_view(),
        name='dois-list'
    ),
]
