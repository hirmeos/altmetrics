from nameko.events import EventDispatcher
from nameko.rpc import rpc

from flask import current_app


class ServiceHandler:

    def __init__(self, service):
        self.service = service

    def send(self, content):
        """ Send content over RPC to a service, triggering pre and post actions.

        Args:
            content (object): Content to send over RPC to connected service.
        """

        prepared_content = self.service.pre_send(content)

        with current_app.config.get('CLUSTER_RPC') as cluster_rpc:
            running_service = getattr(cluster_rpc, self.service.name)
            running_service.send(prepared_content)

        self.service.post_send(content)


class MetricsAPIServiceDispatcher:
    """ Nameko dispatcher to send out metrics to the Metrics API. """

    name = 'metrics_api_service'
    dispatch = EventDispatcher()

    @staticmethod
    def pre_send(data):
        return data

    @rpc
    def send(self, data):
        """ Send entry data as a notification to the Metrics-API. """
        self.dispatch('new_entry', data)

    @staticmethod
    def post_send(data):
        pass
