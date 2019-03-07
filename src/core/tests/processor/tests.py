import unittest
from unittest.mock import patch
from urllib.parse import unquote

from processor.logic import (
    check_wikipedia_event,
    get_doi_deposit_date,
    get_language_from_wiki_url,
    get_mailto,
    get_non_wikipedia_references,
    get_wiki_page_title,
    get_wikimedia_call_info,
    get_wikipedia_references,
    is_in_references,
    is_wikipedia_url,
    set_generic_twitter_link,
)
from .variables import (
    wiki_json,
    wiki_reference_simple,
    wiki_reference_encoded,
    MockEvent,
    MockUri,
    MockWikipediaPage,
)


class WikipediaTestCase(unittest.TestCase):

    base_netloc = 'sv.wikipedia.org'
    base_url = f'https://{base_netloc}/wiki'

    page_title = 'Festival_Romanistica'  # Page titles
    page_title_encoded = 'Fanny_Ambj%C3%B6rnsson'

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
        mock_requests.get().json.return_value = wiki_json
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
        wiki_client.WikipediaPage.return_value = MockWikipediaPage([])
        page_url = f'{self.base_url}/{self.page_title}'
        uri_obj = MockUri(raw='10.5334/baj')
        event_obj = MockEvent(
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
        wiki_client.WikipediaPage.return_value = MockWikipediaPage([])
        page_url = f'https://commons.wikimedia.org/{self.page_title}'
        uri_obj = MockUri(raw='10.5334/baj')
        event_obj = MockEvent(
            subject_id=page_url,
            uri=uri_obj
        )
        check_wikipedia_event(event_obj)

        refs_function.assert_called_with(page_url)

    def test_is_in_references_simple(self):
        """ Check that function can identify doi inside a reference list."""
        self.assertTrue(
            is_in_references(
                references=wiki_reference_simple.references,
                doi=wiki_reference_simple.doi
            )
        )
        self.assertFalse(  # Check the function does not always return True
            is_in_references(
                references=wiki_reference_simple.references,
                doi='10.21401/not/a/doi'
            )
        )

    def test_is_in_references_encoded(self):
        """ Check that function can identify doi inside a reference
        list, where the doi is encoded for a URL.
        """
        self.assertTrue(
            is_in_references(
                references=wiki_reference_encoded.references,
                doi=wiki_reference_encoded.doi
            )
        )
        self.assertFalse(  # Check the function does not always return True
            is_in_references(
                references=wiki_reference_encoded.references,
                doi='10.21401/not/a/doi'
            )
        )

    def test_set_generic_twitter_link_with_id(self):
        """ Check that function converts twitter ID to correct URL."""
        self.assertEqual(
            set_generic_twitter_link('123456789'),
            'https://twitter.com/i/web/status/123456789'
        )

    def test_set_generic_twitter_link_with_url(self):
        """ Check that function converts twitter URL to correct URL."""
        twitter_url = 'https://twitter.com/AnyUserAccount/status/123456789'
        self.assertEqual(
            set_generic_twitter_link(twitter_url),
            'https://twitter.com/i/web/status/123456789'
        )

    # @patch('flask.current_app')
    # def test_get_mailto_returns_app_context_email(self, flask_app):
    #     """ Test that function returns the default email inside app context."""
    #     flask_app.config.return_value = {'TECH_EMAIL': 'admin.user@mail.org'}
    #     test_mail = get_mailto(default_email='test.user@mail.org')
    #     self.assertEqual(test_mail, 'admin.user@mail.org')

    def test_get_mailto_returns_correct_default(self):
        """ Test that function returns the default email outside app context."""
        test_mail = get_mailto(default_email='test.user@mail.org')
        self.assertEqual(test_mail, 'test.user@mail.org')

    # @patch('requests.get')
    # def test_get_doi_deposit_date(self, get_request):

