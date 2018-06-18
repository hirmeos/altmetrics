from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_swagger.views import get_swagger_view

from processor.models import (
    Event,
    Scrape,
    Uri,
    UriUpload,
    Url,
)

from .serializers import (
    UriUploadSerializer,
    EventSerializer,
    ScrapeSerializer,
    UriSerializer,
    UrlSerializer
)

schema_view = get_swagger_view(title='HIRMEOS Metrics API')


class UriViewSet(viewsets.ModelViewSet):
    """ API endpoint to display URIs. """

    permission_classes = (IsAuthenticated,)
    queryset = Uri.objects.all()
    serializer_class = UriSerializer


class DoiUploadViewSet(viewsets.ModelViewSet):
    """ API endpoint to display DOI Uploads. """

    permission_classes = (IsAuthenticated,)
    serializer_class = UriUploadSerializer
    queryset = UriUpload.objects.all()

    def get_queryset(self):
        """ Return objects owned by user. """
        return [
            upload for upload in UriUpload.objects.all()
            if upload.owner() == self.request.user
        ]


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint to display Events. """

    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ScrapeViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint to display Scrapes. """

    permission_classes = (IsAuthenticated,)
    queryset = Scrape.objects.all()
    serializer_class = ScrapeSerializer


class UrlViewSet(viewsets.ModelViewSet):
    """ API endpoint to display URLs. """

    permission_classes = (IsAuthenticated,)
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    def get_queryset(self):
        """ Return objects owned by user. """

        return [u for u in Url.objects.all() if self.request.user in u.owners()]


class AltmetricViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint to display Altmetrics. """

    # permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        params = self.request.query_params

        if (
                params.get('view') == 'source' and
                params.get('source') == 'hypothesis'
        ):
            qs = self.queryset.filter(
                uri='info:doi:{uri}'.format(uri=params.get('uri'))
            )

            return qs

        return self.queryset
