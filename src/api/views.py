from logging import getLogger
from urllib.parse import urlencode

from flask import Blueprint, abort, g, jsonify, request
from flask.views import MethodView
from flask_api.status import HTTP_404_NOT_FOUND
from flask_login import current_user
from flask_security.decorators import http_auth_required

from core import db
from processor.models import (
    Uri,
    Url,
    Event,
)
from user.decorators import account_approved, token_authenticated
from user.tokens import issue_token

from .logic import get_origin_from_name, queryset_exists
from .serializers import (
    EventSerializer,
    UriSerializer,
)


logger = getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api')


class TokensViewSet(MethodView):
    """ API endpoint to get JWT a API token. """

    @http_auth_required
    @account_approved
    def get(self):
        user = current_user
        if not user:
            abort(401, "Invalid user credentials")

        return issue_token(user=user)  # , lifespan=86400)  # TODO: change back

    @http_auth_required
    @account_approved
    def post(self):
        user = current_user
        if not user:
            abort(401, "Invalid user credentials")

        token = issue_token(user=user)  # , lifespan=86400)  # TODO: change back

        return {
            'status': 'ok',
            'count': 1,
            'code': 200,
            'data': [user.prepare_full_token_details(token)]
        }


bp.add_url_rule(
    '/get_token/',
    strict_slashes=False,
    view_func=TokensViewSet.as_view('get-token')
)


class UriViewSet(MethodView):
    """ API endpoint to post and display URIs. """

    decorators = [token_authenticated]

    serializer_class = UriSerializer

    def get(self):
        schema = self.serializer_class(
            many=True,
            only=('raw', 'urls', 'last_checked')
        )

        query = Uri.query.filter(Uri.users.contains(g.user))

        page = int(request.args.get('page', 1))  # Apply pagination
        per_page = int(request.args.get('per_page', 100))

        query_page = query.paginate(
            page=page,
            per_page=per_page
        )

        uri_data, _ = schema.dump(query_page.items)

        response = {'data': uri_data}
        if query_page.has_next:
            request_args = request.args.copy()
            request_args.setlist('page', [page+1])
            request_args.setlist('per_page', [per_page])
            response.update(
                next=f'{request.base_url}?{urlencode(request_args)}',
            )

        return response

    def post(self):
        """ Register DOIs in the Altmetrics service. Also check if the URLs
        provided, as well as the user making the request, need to be associated
        with the DOI if it already exists.

        Expected format of DOIs:
            [
                {
                    'doi': '10.123/xxxxx'
                    'url': ['www.site.com/booklink', 'www.press.co.za/read'],
                },
                {
                    'doi': '10.456/aaaaa'
                    'url': ['www.site.org/book/doi', 'www.books.gov.uk/read'],
                },
                ... etc
            ]
        """
        doi_list = request.get_json()

        if not doi_list:
            abort_message = 'DOI list not found in request JSON.'
            logger.error(f'Bad Request: {abort_message} JSON: {doi_list}')
            abort(400, abort_message)

        for doi_dict in doi_list:

            try:
                doi_value = doi_dict['doi']
            except KeyError:
                abort_message = 'Identifier "doi" is required for each entry.'
                logger.error(f'Bad Request: {abort_message} JSON: {doi_list}')
                abort(400, abort_message)

            uri = Uri.query.filter(Uri.raw == doi_value).first()

            if not uri:
                uri = Uri(raw=doi_value, last_checked=None)
                uri.users.append(g.user)
                db.session.add(uri)

            elif not queryset_exists(uri.users.filter_by(id=g.user.id)):
                uri.users.append(g.user)

            for raw_url in doi_dict.get('url', []):
                raw_url = raw_url.rstrip('/')  # Avoid duplicates
                if not queryset_exists(Url.query.filter_by(url=raw_url)):
                    associated_url = Url(url=raw_url, uri=uri)
                    db.session.add(associated_url)

        db.session.commit()

        return jsonify(200)


bp.add_url_rule(
    '/uriset/',
    strict_slashes=False,
    view_func=UriViewSet.as_view('uri-set')
)


class UriGet(MethodView):
    """ API endpoint to fetch a single URIs. """

    decorators = [token_authenticated]
    serializer_class = UriSerializer

    def get(self, uri):
        schema = self.serializer_class(
            many=False,
            only=('raw', 'urls', 'last_checked')
        )
        uri_data, _ = schema.dump(
            Uri.query.filter(
                Uri.users.contains(g.user),
                Uri.raw == uri
            ).one_or_none()
        )
        if uri_data:
            return uri_data

        return (
            {'message': f'No URI {uri} associated with your account.'},
            HTTP_404_NOT_FOUND,
        )


bp.add_url_rule(
    '/uriset/<path:uri>/',
    strict_slashes=False,
    view_func=UriGet.as_view('uri-get')
)


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
        event_query = Event.query.filter_by(origin=origin.value)
        uri = Uri.query.filter(Uri.raw == request.args.get('uri')).first()
        if uri:
            event_query = event_query.filter(Event.uri == uri)
        event_data, errors = schema.dump(event_query)

        return jsonify(event_data)


bp.add_url_rule(
    '/eventset/',
    strict_slashes=False,
    view_func=EventViewSet.as_view('event-set')
)
