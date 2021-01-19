import unittest

from api.logic import get_origin_from_name, get_uri_prefix
from core.settings import Origins


class LogicTestCase(unittest.TestCase):

    def test_get_origin_from_name(self):
        """ Check that function identifies twitter origin by its name."""
        self.assertEqual(
            get_origin_from_name('twitter'),
            Origins.twitter,
            'Failed to identify twitter origin by name.'
        )

    def test_get_origin_from_name_returns_none_for_unrecognised_origin(self):
        """ Check that function returns None for unknown origin name."""
        self.assertEqual(
            get_origin_from_name('unrecognised'),
            None,
            'Failed to return `None` for unknown origin name.'
        )

    def test_get_uri_prefix_returns_expected_output(self):
        """Ensure function returns correct prefix for all expected uris."""
        expected_prefix = '10.5334'
        uris = [
            f'{expected_prefix}/bbc',
            f'{expected_prefix}/bbc/other-stuff',
        ]

        self.assertEqual(
            set(map(get_uri_prefix, uris)),
            {expected_prefix},
            'Failed to return expected prefix value.'
        )

    def test_get_uri_prefix_returns_expected_output(self):
        """Ensure function returns correct/additional prefix for given uris."""
        expected_prefix = '10.5334'
        unexpected_prefix = '10.9999'
        uris = [
            f'{expected_prefix}/bbc',
            f'{expected_prefix}/bbc/other-stuff',
            f'{unexpected_prefix}/bbc/other-stuff',
        ]

        self.assertNotEqual(
            set(map(get_uri_prefix, uris)),
            {expected_prefix},
            'Failed to return additional prefix provided.'
        )
