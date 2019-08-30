from dataclasses import dataclass, field
from datetime import datetime as dt, timedelta
import jwt
from os import environ

import unittest
from unittest.mock import patch

from core import create_app, db
from user.models import User, Role
from user.tokens import (
    issue_token,
    validate_token
)
from user.tasks import approve_user, send_approval_request


environ['CONFIG'] = 'TestConfig'


@dataclass
class MockUser:
    """Mock user with attributes required for testing."""
    email: str
    first_name: str
    full_name: str
    roles: list = field(default_factory=list)
    approved: bool = False

    def has_role(self, role_value):
        return role_value in self.roles


@patch('user.tokens.current_app')
class TokensTestCase(unittest.TestCase):
    jwt_key = 'n/a'
    jwt_key_2 = 'N/A'
    demo_user = MockUser(
        email='demo@acc.com',
        first_name='The',
        full_name='The User'
    )

    def test_issue_token_creates_a_jwt(self, demo_app):
        """Test that function creates a token that can be decoded."""
        demo_app.config.get.return_value = self.jwt_key
        token = issue_token(self.demo_user)

        self.assertNotEqual(
            jwt.decode(token, self.jwt_key, algorithms=['HS256']),
            None,
            'Invalid token created.'
        )

    def test_issue_token_creates_a_jwt_hat_is_key_specific(self, demo_app):
        """Test that token created cannot be decoded with another key. """
        demo_app.config.get.return_value = self.jwt_key
        token = issue_token(self.demo_user)

        message = 'Failed to create a key-specific token.'
        with self.assertRaises(jwt.DecodeError, msg=message):
            jwt.decode(token, self.jwt_key_2, algorithms=['HS256'])

    def test_issue_token_with_lifespan(self, demo_app):
        """Test that token expires if created with a lifespan. """
        demo_app.config.get.return_value = self.jwt_key
        token_lifespan = 5
        token = issue_token(self.demo_user, lifespan=token_lifespan)

        decoded_token = jwt.decode(token, self.jwt_key, algorithms=['HS256'])
        expires_at_delta = dt.fromtimestamp(decoded_token['exp']) - dt.now()
        self.assertLessEqual(
            expires_at_delta,
            timedelta(seconds=token_lifespan),
            'Failed to create token with a lifespan.'
        )

    def test_validate_token(self, demo_app):
        """Test that function recognises a token as valid. """
        demo_app.config.get.return_value = self.jwt_key
        token = jwt.encode({}, self.jwt_key, algorithm='HS256')

        self.assertTrue(
            validate_token(token)[0],
            'Failed to validate token.'
        )

    def test_validate_token_returns_false_for_invalid_token(self, demo_app):
        """Test that function returns False for invalid tokens. """
        demo_app.config.get.return_value = self.jwt_key
        token = jwt.encode({}, self.jwt_key_2, algorithm='HS256')

        self.assertFalse(
            validate_token(token)[0],
            'Failed to recognise invalidate token.'
        )


class TasksTestCase(unittest.TestCase):
    demo_user = MockUser(
        email='demo@acc.com',
        first_name='The',
        full_name='The User',
        roles=['x']
    )

    @patch('user.tasks.configure_mail_body')
    @patch('user.tasks.current_app')
    @patch('user.tasks.db')
    @patch('user.tasks.mail')
    @patch('user.tasks.User')
    @patch('user.tasks.Role')
    def test_approve_user(
            self,
            role_class,
            user_class,
            task_mail,
            task_db,
            task_app,
            configure_mail_function
    ):
        task_app.config.get.return_value = 'tech@test.com'
        user_class.query.get.return_value = self.demo_user
        role_class.query.get.return_value = 'x'

        approve_user(0, 1, 2, {})

        configure_mail_function.assert_called()
        task_db.session.commit.assert_called()
        task_mail.send.assert_called()


class TasksIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('user.tasks.configure_mail_body')
    @patch('user.tasks.mail')
    def test_approve_user_(
            self,
            task_mail,
            configure_mail_function
    ):
        default_role = Role(name='default', description='n/a')
        new_role = Role(name='new role', description='n/a')

        db.session.add(default_role)
        db.session.add(new_role)

        user_1 = User(
            username='testuser01',
            email='test@user.com',
            password='test_pw',
            first_name='Test',
            last_name='User',
            institution='TEST CI',
        )
        user_1.roles.append(default_role)
        db.session.add(user_1)
        db.session.commit()

        with self.app_context:
            approve_user(user_1.id, default_role.id, new_role.id, {})

        configure_mail_function.assert_called()
        task_mail.send.assert_called()

        self.assertTrue(user_1.is_approved, 'Failed to approve user')
        self.assertEqual(
            user_1.roles,
            [new_role],
            'Failed to set Role correctly'
        )
