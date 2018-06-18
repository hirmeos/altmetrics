from django.conf import settings
from django.contrib.auth.models import User

from processor.models import Measure, UriUpload


def users_from_uploads(doi):
    """ Generate a list of users that uploaded a csv that created the DOI.

      Parameters:
        doi (Doi): the doi used to generate a list of users from

      Returns:
        list: Users that uploaded a CSV with the doi in it.
    """

    uploads = [doiup.upload for doiup in UriUpload.objects.filter(doi=doi)]
    users = None

    for upload in uploads:
        if users:
            users |= User.objects.filter(csvupload=upload)
        else:
            users = User.objects.filter(csvupload=upload)

    return users


def event_generator(uri, namespaces, scrape):
    """ Generator of events for each of the DOIs being processed.

        Iterates over the namespaces, over the allowed origins for each
        namespace and over all the different providers available (from plugins)
        for each origin, and fetches events.

       Args:
           uri (object): Uri from ORM.
           namespaces (list): Namespaces to iterate on from ORM.
           scrape (object): Scrape from ORM, not saved to database (yet).

       Returns:
        generator: yields a list of events for each plugin, which if turned
            into a list will be a list of lists of events.
    """

    for namespace in namespaces:
        for source in namespace.allowed_origins:

            measure = Measure.objects.get(
                namespace=namespace,
                source__name=source
            )

            for provider in settings.ORIGINS.get(source):
                yield provider.PROVIDER.process(uri, source, scrape, measure)
