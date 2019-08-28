import unittest
from unittest.mock import call, patch

from core.logic import (
    configure_mail_body,
    get_enum_by_value,
    get_enum_by_name,
)
from .variables import MockMail, MockEnum


class LogicTestCase(unittest.TestCase):

    def test_get_enum_by_name(self):
        """ Check that function identifies enum by its name."""
        self.assertEqual(
            get_enum_by_name(MockEnum, 'demo_1'),
            MockEnum.demo_1,
            'Failed to identify enum by its name.'
        )

    def test_get_enum_by_name_returns_none_for_unrecognised_enum(self):
        """ Check that function returns None for unknown name."""
        self.assertEqual(
            get_enum_by_name(MockEnum, 'unrecognised'),
            None,
            'Failed to return `None` for unknown enum name.'
        )

    def test_get_enum_by_value(self):
        """Check that function returns correct enum, based on its value."""
        self.assertEqual(
            get_enum_by_value(MockEnum, 3),
            MockEnum.demo_3,
            'Failed to identify enum by its value.'
        )

    def test_get_enum_by_value_retuns_none_for_unrecognised_value(self):
        """Check that function returns none for unknown enum value."""
        self.assertEqual(
            get_enum_by_value(MockEnum, 99),
            None,
            'Failed to return `None` for unknown enum value.'
        )

    @patch('core.logic.render_template')
    def test_configure_mail_body(self, render_function):
        """Check that function renders both body and html."""

        message_body = 'Message body'
        demo_template = 'demo_template'
        message_kwargs = {'name': 'Username', 'values': 'not important'}

        render_function.return_value = message_body

        mail_obj = MockMail()

        configure_mail_body(
            msg=mail_obj,
            template_name=demo_template,
            context=message_kwargs
        )

        call_list = [
            call(f'mail/{demo_template}.txt', **message_kwargs, ),
            call(f'mail/{demo_template}.html', **message_kwargs, )
        ]
        render_function.assert_has_calls(call_list)

        self.assertEqual(mail_obj.html, message_body, 'Message body not set')
        self.assertEqual(mail_obj.body, message_body, 'Message html not set')
