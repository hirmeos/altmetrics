from flask import current_app


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
    event_dict = {}     # keep track of events across plugins
    for origin, plugins in current_app.config.get("ORIGINS").items():
        for plugin in plugins:
            event_dict, events = plugin.PROVIDER.process(
                uri,
                origin,
                scrape,
                last_check,
                event_dict
            )
            yield events
