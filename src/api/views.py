from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from processor import models as processor_models
from .serializers import DoiSerializer, EventSerializer, ScrapeSerializer


class DoiViewSet(viewsets.ModelViewSet):
    """ API endpoint to display DOIs. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Doi.objects.all()
    serializer_class = DoiSerializer


class EventViewSet(viewsets.ModelViewSet):
    """ API endpoint to display Events. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Event.objects.all()
    serializer_class = EventSerializer


class ScrapeViewSet(viewsets.ModelViewSet):
    """ API endpoint to display Scrapes. """

    permission_classes = (IsAuthenticated,)
    queryset = processor_models.Scrape.objects.all()
    serializer_class = ScrapeSerializer
