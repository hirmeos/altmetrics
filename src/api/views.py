from flask import Blueprint, abort, g, jsonify, request
from flask.views import MethodView

from core import db
from models import (
    Uri,
    Url,
    Event,
    User,
)
from user.decorators import token_authenticated
from user.tokens import issue_token

from .logic import get_origin_from_name, queryset_exists
from .serializers import (
    EventSerializer,
    UriSerializer,
)


bp = Blueprint('api', __name__, url_prefix='/api')


class TokensViewSet(MethodView):
    """ API endpoint to get JWT a API token. """

    def post(self):
        request_data = request.get_json()
        user = User.query.filter_by(
            email=request_data.get('email'),
        ).first()

        password = request_data.get('password')
        if not (user and user.verify_and_update_password(password)):
            abort(401, "Invalid user credentials")

        return issue_token(email=user.email)


bp.add_url_rule('/get_token', view_func=TokensViewSet.as_view('get-token'))


class UriViewSet(MethodView):
    """ API endpoint to post and display URIs. """

    decorators = [token_authenticated]

    serializer_class = UriSerializer

    def get(self):
        schema = self.serializer_class(
            many=True,
            only=('raw', 'urls', 'last_checked')
        )
        uri_data, errors = schema.dump(
            Uri.query.filter(Uri.users.contains(g.user))
        )
        return uri_data

    def post(self):
        """ Register DOIs in the Altmetrics service. Also check if the URLs
        provided, as well as the user making the request, need to be associated
        with the DOI if it already exists.

        Expected format of DOIs:
            [
                {
                    doi: '10.123/xxxxx'
                    url: ['www.site.com/booklink', 'www.press.co.za/read'],
                },
                {
                    doi: '10.456/aaaaa'
                    url: ['www.site.org/book/doi', 'www.books.gov.uk/read/doi'],
                },
                ... etc
            ]
        """
        doi_list = request.get_json()

        for doi_dict in doi_list:

            uri = Uri.query.filter(Uri.raw == doi_dict['doi']).first()

            if not uri:
                uri = Uri(raw=doi_dict['doi'], last_checked=None)
                uri.users.append(g.user)
                db.session.add(uri)

            elif not queryset_exists(uri.users.filter_by(id=g.user.id)):
                uri.users.append(g.user)

            for raw_url in doi_dict.get('url', []):
                if not queryset_exists(Url.query.filter_by(url=raw_url)):
                    associated_url = Url(url=raw_url, uri=uri)
                    db.session.add(associated_url)

        db.session.commit()

        return jsonify(200)


bp.add_url_rule('/uriset', view_func=UriViewSet.as_view('uri-set'))


class EventViewSet(MethodView):
    """ API endpoint to display Events. """

    decorators = [token_authenticated]

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
