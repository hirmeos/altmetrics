from rest_framework import viewsets

from processor import models as processor_models
from .serializers import DoiSerializer, EventSerializer, ScrapeSerializer


class DoiViewSet(viewsets.ModelViewSet):
    """ API endpoint to display DOIs. """

    queryset = processor_models.Doi.objects.all()
    serializer_class = DoiSerializer


class EventViewSet(viewsets.ModelViewSet):
    """ API endpoint to display Events. """

    queryset = processor_models.Event.objects.all()
    serializer_class = EventSerializer


class ScrapeViewSet(viewsets.ModelViewSet):
    """ API endpoint to display Scrapes. """

    queryset = processor_models.Scrape.objects.all()
    serializer_class = ScrapeSerializer
