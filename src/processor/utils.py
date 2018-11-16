from flask import current_app
# from models import User   # TODO: Add user model


# def users_from_uploads(doi):
#     """ Generate a list of users that uploaded a csv that created the DOI.
#
#       Parameters:
#         doi (Doi): the doi used to generate a list of users from
#
#       Returns:
#         list: Users that uploaded a CSV with the doi in it.
#     """
#
#     uploads = [doiup.upload for doiup in UriUpload.objects.filter(doi=doi)]
#     users = None
#
#     for upload in uploads:
#         if users:
#             users |= User.objects.filter(csvupload=upload)
#         else:
#             users = User.objects.filter(csvupload=upload)
#
#     return users


def event_generator(uri, scrape, last_check):
    """ Generator of events for each of the DOIs being processed.

        Iterates over the origins for each plugin, and uses Provider from the
        plugin to fetch (yield) events for the DOI and origin.

       Args:
           uri (object): Uri from ORM.
           scrape (object): Scrape from ORM, not saved to database (yet).
           last_check (datetime): when this uri was last successfully scraped.

       Returns:
            generator: yields a generator of events for each plugin, which if
            turned into a list will be a list of lists of events.
    """
    for origin, plugins in current_app.config.get("ORIGINS").items():
        for plugin in plugins:
            yield plugin.PROVIDER.process(uri, origin, scrape, last_check)
