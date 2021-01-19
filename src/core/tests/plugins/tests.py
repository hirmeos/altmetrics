import unittest

from core import create_app, db, plugins
from core.variables import StaticProviders
from plugins.crossref_event_data.schema import determine_doi
from processor.models import Uri

from .variables import (
    build_events_input,
    dois_expected,
    dois_unexpected,
    event_data_expected_events,
    event_data_unexpected_events,
    expected_build_type_profile,
    expected_valid,
    prebuild_expected_division,
)


dois_all = dois_unexpected.copy()
dois_all.extend(dois_expected)
dois_expected_ids = [_[0] for _ in dois_expected]

event_data_all_events = event_data_unexpected_events.copy()
event_data_all_events.extend(event_data_expected_events)


class EventDataPluginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.provider = plugins.get_plugin(
            StaticProviders.crossref_event_data
        ).PROVIDER

        db.create_all()
        for uri_id, uri_raw in dois_all:
            db.session.add(Uri(id=uri_id, raw=uri_raw))

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_event_data_plugin_validate_correct_number(self):
        """Test that validator marks the correct number of events as valid."""
        self.provider._add_validator_context(
            provider=self.provider.provider.value,
            scrape_id=0
        )
        valid = list(self.provider._validate(event_data_all_events))

        self.assertEqual(
            len(valid),
            len(event_data_expected_events),
            'Incorrect number of events marked as valid.',
        )

    def test_event_data_plugin_validate_correct_content(self):
        """Test that validator contains the correct valid events."""
        self.provider._add_validator_context(
            provider=self.provider.provider.value,
            scrape_id=0
        )
        valid = self.provider._validate(event_data_all_events)

        self.assertEqual(
            list(sorted(valid, key=lambda x: x['external_id'])),
            list(sorted(expected_valid, key=lambda x: x['external_id'])),
            'Not all expected events have been marked as valid/invalid.',
        )

    def test_event_data_plugin_pre_build_by_uri(self):
        """Test that prebuild correctly divides events by URI ID."""
        built_events = self.provider._pre_build(expected_valid)

        self.assertEqual(
            list(sorted(built_events.keys())),
            list(sorted(dois_expected_ids)),
            'Prebuilt event keys not correctly divided as expected.',
        )

    def test_event_data_plugin_pre_build_by_uri_and_origin(self):
        """Test that prebuild correctly divides events by URI and origin."""

        built_events = self.provider._pre_build(expected_valid)

        prebuild_divisions = []
        for key, values in built_events.items():
            prebuild_divisions.append(
                (key, list(sorted(map(lambda x: x.name, values.keys()))))
            )  # getting a bit ridiculous at this point

        self.assertEqual(
            prebuild_expected_division,
            prebuild_divisions,
            'Prebuilt event nested keys not correctly divided as expected.',
        )

    def test_event_data_plugin_build(self):
        """Testing that the output structure is correct."""
        uri_id, origin, events = build_events_input

        output_events = self.provider._build(
            event_data=events,
            uri_id=uri_id,
            origin=origin,
        )

        type_check = list(map(type, output_events.keys()))
        for value in output_events.values():
            type_check.extend(list(map(type, value)))

        self.assertEqual(
            type_check,
            expected_build_type_profile,
            'Built type check failed.',
        )


class LogicTestCase(unittest.TestCase):

    def test_determine_doi_extracts_doi_correctly(self):
        """ Check that function identifies twitter origin by its name."""

        target_doi = '10.5334/bha.20202'
        event_data_doi = f'https://doi.org/{target_doi}'

        self.assertEqual(
            determine_doi(event_data_doi),
            target_doi,
            'Failed to determine correct DOI from event data response.'
        )
