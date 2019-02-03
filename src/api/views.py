import json

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from core import db
from models import (
    Uri,
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
        json_input = request.get_json()

        doi_list = json_input.get("doi_list")

        for raw_uri in doi_list:
            new_uri = Uri(raw=raw_uri, last_checked=None)
            db.session.add(new_uri)

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
