from rest_framework import serializers

from processor import models as processor_models


class DoiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = processor_models.Doi
        fields = 'doi', 'last_checked'


class ScrapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = processor_models.Scrape
        fields = 'start_date', 'end_date'


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = processor_models.Event
        fields = (
            'external_id',
            'source_id',
            'source',
            'created_at',
            'content',
            'scrape',
            'doi',
        )
    scrape = ScrapeSerializer()
    doi = DoiSerializer()
