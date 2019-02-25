import unittest
from unittest.mock import patch
from urllib.parse import unquote

from processor.logic import (
    check_wikipedia_event,
    get_wiki_page_title,
    get_wikipedia_references,
    get_language_from_wiki_url,
    get_non_wikipedia_references,
    get_wikimedia_call_info,
    is_wikipedia_url,
)


class WikipediaTestCase(unittest.TestCase):

    base_netloc = 'sv.wikipedia.org'
    base_url = f'https://{base_netloc}/wiki'

    page_title = 'Festival_Romanistica'  # Page titles
    page_title_encoded = 'Fanny_Ambj%C3%B6rnsson'

    class MockUri(object):
        def __init__(self, raw):
            self.raw = raw

    class MockEvent(object):
        def __init__(self, subject_id, uri):
            self.subject_id = subject_id
            self.uri = uri

    class MockWikipediaPage(object):
        def __init__(self, references):
            self.references = references

    def test_get_wiki_page_title(self):
        """ Check function returns the title of a wikipedia page, based on
        its url.
        """
        page_url = f'{self.base_url}/{self.page_title}'
        page_title = unquote(self.page_title)

        self.assertEqual(
            get_wiki_page_title(page_url),
            page_title,
            'Failed to return correct wiki page title.'
        )

    def test_get_wiki_page_title_encoded(self):
        """ Check function returns the title of a wikipedia page, based on
        its url, taking URL encoding into consideration.
        """
        encoded_url = f'{self.base_url}/{self.page_title_encoded}'
        page_title = unquote(self.page_title_encoded)

        self.assertEqual(
            get_wiki_page_title(encoded_url),
            page_title,
            'Failed to return correct encoded wiki page title.'
        )

    def test_get_wiki_call_info(self):
        """ Check function returns expected url and that the correct
        page title is in the API call parameters returned.
        """
        encoded_url = f'{self.base_url}/{self.page_title_encoded}'
        page_title = unquote(self.page_title_encoded)
        expected_url = f'https://{self.base_netloc}/w/api.php'

        url, params = get_wikimedia_call_info(encoded_url)
        self.assertEqual(
            url,
            expected_url,
            'Failed to create expected URL for call to wiki API.'
        )
        self.assertEqual(params.get('titles'), page_title)

    def test_is_wikipedia_url(self):
        """ Check that function returns True for a wikimedia URL."""
        wiki_url = 'https://en.wikipedia.org/wiki/wikipedia_page'
        self.assertTrue(
            is_wikipedia_url(wiki_url),
            'Failed to identify wikipedia page.'
        )

    def test_is_wikipedia_url_rejects_non_wiki_url(self):
        """ Check that function returns False for a non-wikimedia URL."""
        non_wiki_url = 'https://not.wikipedia.org/wiki/wikipedia_page'
        self.assertFalse(
            is_wikipedia_url(non_wiki_url),
            'Failed to identify non-wikipedia page.'
        )

    def test_get_language_from_wiki_url(self):
        """ Check that function returns correct two-letter language code from a
        wikimedia URL.
        """
        wiki_url = 'https://de.wikipedia.org/wiki/wikipedia_seite'
        self.assertEqual(
            get_language_from_wiki_url(wiki_url),
            'de',
            'Failed to identify correct language code for wiki page.'
        )

    @patch('processor.logic.wikipedia')
    def test_get_wikipedia_references(self, wiki_client):
        """ Check that wikipedia client is called when getting wikipedia
        references.
        """
        url = 'https://en.wikipedia.org/wiki/wikipedia_page'
        get_wikipedia_references(url)

        wiki_client.set_lang.assert_called_with('en')
        wiki_client.WikipediaPage.assert_called()

    @patch('processor.logic.requests')
    def test_get_non_wikipedia_references(self, mock_requests):
        """ Check that requests library is called when getting non-wikipedia
        references.
        """
        # This will need to be moved somewhere more suitable - and simplified.
        mock_requests.get().json.return_value = {
            'batchcomplete': '',
            'query': {
                'normalized': [
                    {
                        'from': 'The_battle_for_open',
                        'to': 'The battle for open'
                    }
                ],
                'pages': {
                    '1950647': {
                        'pageid': 1950647,
                        'ns': 0,
                        'title': 'The battle for open',
                        'extlinks': [
                            {'*': 'http://dx.doi.org/10.5334/bam'},
                            {'*': 'http://creativecommons.org/licenses/by/3.0/'}
                        ]
                    }
                }
            }
        }
        url = 'https://wikisource.org/wiki/Index:Anything.pdf'
        get_non_wikipedia_references(url)

        mock_requests.get.assert_called()

    @patch('processor.logic.wikipedia')
    @patch('processor.logic.get_wikipedia_references')
    def test_calls_get_wikipedia_refs_if_wikipedia_url(
            self,
            refs_function,
            wiki_client,
    ):
        """ Check that get_wikipedia_references() function is called if a
        wikipedia URL is passed.
        """
        wiki_client.WikipediaPage.return_value = self.MockWikipediaPage([])
        page_url = f'{self.base_url}/{self.page_title}'
        uri_obj = self.MockUri(raw='10.5334/baj')
        event_obj = self.MockEvent(
            subject_id=page_url,
            uri=uri_obj
        )
        check_wikipedia_event(event_obj)

        refs_function.assert_called_with(page_url)

    @patch('processor.logic.wikipedia')
    @patch('processor.logic.get_non_wikipedia_references')
    def test_calls_get_non_wikipedia_refs_if_non_wiki_url(
            self,
            refs_function,
            wiki_client,
    ):
        """ Check that get_non_wikipedia_references() function is called if a
        non-wikipedia URL is passed.
        """
        wiki_client.WikipediaPage.return_value = self.MockWikipediaPage([])
        page_url = f'https://commons.wikimedia.org/{self.page_title}'
        uri_obj = self.MockUri(raw='10.5334/baj')
        event_obj = self.MockEvent(
            subject_id=page_url,
            uri=uri_obj
        )
        check_wikipedia_event(event_obj)

        refs_function.assert_called_with(page_url)
