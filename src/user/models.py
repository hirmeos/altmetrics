from datetime import datetime

from sqlalchemy.orm import validates

from validators import email as email_validator

from flask_security import RoleMixin, UserMixin

from core.database import (  # not sure how I feel about this
    backref,
    relationship,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Model,
    String,
    Table,
)


"""Helper table, linking Users to URIs."""
uris_users = Table(
    'uris_users',
    Column('uri_id', Integer, ForeignKey('uri.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

"""Helper table, linking Users to Roles."""
roles_users = Table(
    'roles_users',
    Column('user_id', Integer(), ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer(), ForeignKey('role.id'), primary_key=True)
)


class Role(Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return self.name


class User(Model, UserMixin):
    """Users who upload DOIs."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)

    active = Column(Boolean())
    approved = Column(Boolean(), default=False)
    confirmed_at = Column(DateTime())
    roles = relationship(
        'Role',
        secondary=roles_users,
        backref=backref('users', lazy='dynamic')
    )
    uris = relationship(
        'Uri',
        secondary=uris_users,
        backref=backref('users', lazy='dynamic')
    )
    # Maybe create a model mixin that has this functionality for all models?
    date_created = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, onupdate=datetime.now)

    @validates('email')
    def valid_uri(self, key, email):
        assert email_validator(email)
        return email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_approved(self):
        return self.approved

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

    def prepare_full_token_details(self, token):
        return {
            'surname': self.last_name,
            'name': self.first_name,
            'authority': 'admin' if self.has_role('admin') else 'user',
            'token': token,
            'email': self.email,
        }
