from rest_framework import serializers

from processor.models import Uri, Url, Scrape, Event, UriUpload


class UriSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Uri
        fields = 'raw', 'last_checked'


class UriUploadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UriUpload
        fields = 'uri',

    uri = UriSerializer()


class ScrapeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Scrape
        fields = 'start_date', 'end_date'


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = (
            'value',
            'external_id',
            'origin_id',
            'created_at',
            'content',
            'uri',
            'scrape',
        )

    scrape = ScrapeSerializer()


class UrlSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Url
        fields = 'url', 'uri'

    uri = UriSerializer()
