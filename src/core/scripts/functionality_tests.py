"""This is a script that does not form part of normal testing, but can be
used as a starting point when trying to test features that normally run as
part of plugins. For example, twitter searches.
"""

from plugins.twitter import PROVIDER as provider
from TwitterSearch import TwitterSearchOrder


def test_twitter_search(keywords):
    """Test using the twitter client to search for keywords.

    Args:
        keywords (list): Keywords to search

    Returns:
        list: serializer dumps of all results returned by Twitter

    """
    if not provider.client:
        provider.client = provider.instantiate_client()

    provider._add_validator_context(  # test values
        uri_id=1111111111111111,
        origin=1,
        provider=1,
        scrape_id=1
    )

    tw_search_order = TwitterSearchOrder()
    tw_search_order.set_keywords(keywords)

    results = provider.client.search_tweets_iterable(tw_search_order)

    return provider._validate(results)
