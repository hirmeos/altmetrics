import unittest

from api.logic import get_origin_from_name
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
