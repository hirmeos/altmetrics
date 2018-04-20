from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from processor import models as processor_models
from .serializers import (
    DoiSerializer,
    DoiUploadSerializer,
    EventSerializer,
    ScrapeSerializer,
    UrlSerializer
)


class DoiViewSet(viewsets.ModelViewSet):
    """ API endpoint to display DOIs. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Doi.objects.all()
    serializer_class = DoiSerializer

    def get_queryset(self):
        """ Return objects owned by user. """

        return [
            doi for doi in processor_models.Doi.objects.all()
            if self.request.user in doi.owners()
        ]


class DoiUploadViewSet(viewsets.ModelViewSet):
    """ API endpoint to display DOI Uploads. """

    permission_classes = (IsAuthenticated,)
    serializer_class = DoiUploadSerializer
    queryset = processor_models.DoiUpload.objects.all()

    def get_queryset(self):
        """ Return objects owned by user. """
        return [
            doiupload for doiupload in processor_models.DoiUpload.objects.all()
            if doiupload.owner() == self.request.user
        ]


class EventViewSet(viewsets.ModelViewSet):
    """ API endpoint to display Events. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        """ Return objects owned by user. """

        return [
            event for event in processor_models.Event.objects.all()
            if self.request.user in event.owners()
        ]


class ScrapeViewSet(viewsets.ModelViewSet):
    """ API endpoint to display Scrapes. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Scrape.objects.all()
    serializer_class = ScrapeSerializer


class UrlViewSet(viewsets.ModelViewSet):
    """ API endpoint to display URLs. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Url.objects.all()
    serializer_class = UrlSerializer

    def get_queryset(self):
        """ Return objects owned by user. """

        return [
            url for url in processor_models.Url.objects.all()
            if self.request.user in url.owners()
        ]
