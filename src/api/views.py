import json

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from models import (
    Uri,
)

from .serializers import (
    UriSerializer,
)

from models import db

bp = Blueprint('api', __name__, url_prefix='/api')


#
# api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api')

# # Example of MethodView
# class UserAPI(MethodView):
#
#     def get(self):
#         users = User.query.all()
#         ...
#
#     def post(self):
#         user = User.from_form_data(request.form)
#         ...
#
# app.add_url_rule('/users/', view_func=UserAPI.as_view('users'))


# def register_api(view, endpoint, url, pk='id', pk_type='int'):
#     view_func = view.as_view(endpoint)
#     app.add_url_rule(url, defaults={pk: None},
#                      view_func=view_func, methods=['GET',])
#     app.add_url_rule(url, view_func=view_func, methods=['POST',])
#     app.add_url_rule(
#         f'{url}<{pk_type}:{pk}>',
#         view_func=view_func,
#         methods=['GET', 'PUT', 'DELETE']
#     )
#
#
# register_api(UserAPI, 'user_api', '/users/', pk='user_id')


class UriViewSet(MethodView):
    """ API endpoint to display URIs. """

    # permission_classes = (IsAuthenticated,)  # TODO

    queryset = Uri.query.all()
    serializer_class = UriSerializer

    def get(self):
        schema = self.serializer_class(many=True, only=('raw', 'last_checked'))
        uri_data, errors = schema.dump(self.queryset)
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


# TODO: Update this
# class DoiUploadViewSet(viewsets.ModelViewSet):
#     """ API endpoint to display DOI Uploads. """
#
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UriUploadSerializer
#     queryset = UriUpload.objects.all()
#
#     def get_queryset(self):
#         """ Return objects owned by user. """
#         return [
#             upload for upload in UriUpload.objects.all()
#             if upload.owner() == self.request.user
#         ]


# #
# # Old Django views:
# # TODO: create flask views for these
# class EventViewSet(viewsets.ReadOnlyModelViewSet):
#     """ API endpoint to display Events. """
#
#     permission_classes = (IsAuthenticated,)
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#
#
# class ScrapeViewSet(viewsets.ReadOnlyModelViewSet):
#     """ API endpoint to display Scrapes. """
#
#     permission_classes = (IsAuthenticated,)
#     queryset = Scrape.objects.all()
#     serializer_class = ScrapeSerializer
#
#
# class UrlViewSet(viewsets.ModelViewSet):
#     """ API endpoint to display URLs. """
#
#     permission_classes = (IsAuthenticated,)
#     queryset = Url.objects.all()
#     serializer_class = UrlSerializer
#
#     def get_queryset(self):
#         """ Return objects owned by user. """
#
#         return [u for u in Url.objects.all() if self.request.user in u.owners()]
#
#
# class AltmetricViewSet(viewsets.ReadOnlyModelViewSet):
#     """ API endpoint to display Altmetrics. """
#
#     # permission_classes = (IsAuthenticated,)
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#
#     def get_queryset(self):
#         params = self.request.query_params
#
#         if (
#                 params.get('view') == 'source' and
#                 params.get('source') == 'hypothesis'
#         ):
#             qs = self.queryset.filter(
#                 uri='info:doi:{uri}'.format(uri=params.get('uri'))
#             )
#
#             return qs
#
#         return self.queryset
