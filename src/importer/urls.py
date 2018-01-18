from django.urls import path

from .views import UploadCSVView, UploadsView, SaveUploadView


urlpatterns = [
    path(
        '',
        UploadsView.as_view(),
        name='importer-list'
    ),
    path(
        'new/',
        UploadCSVView.as_view(),
        name='importer-new'
    ),
    path(
        'new/save/<file_name>',
        SaveUploadView.as_view(),
        name='importer-save'
    ),
]
