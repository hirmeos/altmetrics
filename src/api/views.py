import json

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from core import db
from models import (
    Uri,
    Url,
    Event,
)

from .logic import get_origin_from_name
from .serializers import (
    EventSerializer,
    UriSerializer,
)

bp = Blueprint('api', __name__, url_prefix='/api')


class UriViewSet(MethodView):
    """ API endpoint to display URIs. """

    # permission_classes = (IsAuthenticated,)  # TODO

    serializer_class = UriSerializer

    def get(self):
        schema = self.serializer_class(many=True, only=('raw', 'last_checked'))
        uri_data, errors = schema.dump(Uri.query.all())
        return json.dumps(uri_data)

    def post(self):

        """

        !!! Need to authenticate user first and link their account to this
        upload and doi.

        Also, check if the doi exists and add user to this doi if that is the
        case.

        """

        """New expected format of DOIs:
            [
                {
                    doi: '10.123.xxxxx'
                    url: ['www.xxx.com', www.yyy.com],
                },
                {
                    doi: '10.456.aaaaa'
                    url: ['www.aaa.com', www.bbb.com],
                },
                ... etc
            ]
        """
        json_input = request.get_json()

        doi_list = json_input.get("doi_list")

        for doi_dict in doi_list:
            raw_uri = doi_dict['doi']
            new_uri = Uri(raw=raw_uri, last_checked=None)
            db.session.add(new_uri)

            for raw_url in doi_dict.get('url', []):
                associated_url = Url(url=raw_url, uri=new_uri)
                db.session.add(associated_url)

        db.session.commit()

        return jsonify(200)


bp.add_url_rule('/uriset', view_func=UriViewSet.as_view('uri-set'))


class EventViewSet(MethodView):
    """ API endpoint to display Events. """

    # permission_classes = (IsAuthenticated,)  # TODO

    serializer_class = EventSerializer

    def get(self):
        origin = get_origin_from_name(request.args.get('origin').lower())
        schema = self.serializer_class(
            many=True,
            only=('subject_id', 'origin', 'created_at', 'uri')
        )
        event_query = Event.query.filter(
            Event.origin == origin,
        )
        uri = Uri.query.filter(Uri.raw == request.args.get('uri')).first()
        if uri:
            event_query = event_query.filter(Event.uri == uri)
        event_data, errors = schema.dump(event_query)

        return event_data


bp.add_url_rule('/eventset/', view_func=EventViewSet.as_view('event-set'))
