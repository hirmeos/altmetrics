from datetime import datetime
import re

from sqlalchemy.dialects.postgresql import HSTORE, ENUM
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import validates

from validators import (
    url as url_validator,
    email as email_validator
)

from flask_security import RoleMixin, UserMixin

from core import db
from core.settings import StaticProviders, Origins

Boolean = db.Boolean  # Alias common db types.
Column = db.Column
DateTime = db.DateTime
ForeignKey = db.ForeignKey
Integer = db.Integer
Model = db.Model
String = db.String
Table = db.Table
backref = db.backref
relationship = db.relationship


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


class User(Model, UserMixin):
    """Users who upload DOIs."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))

    active = Column(Boolean())
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

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'


class Uri(Model):
    """DOI to be scraped.

    Columns
    -------
    raw:
        String representation of doi/uri.
    last_checked:
        datetime when scraped was triggered for this uri.
    """

    __tablename__ = 'uri'

    id = Column(Integer, primary_key=True)
    raw = Column(String(50), unique=True, nullable=False)
    last_checked = Column(DateTime)

    # Child Relationships
    deleted_events = relationship('DeletedEvent', backref='uri')
    errors = relationship('Error', backref='uri')
    events = relationship('Event', backref='uri')
    urls = relationship('Url', backref='uri')

    metrics = relationship('Metric', uselist=False, backref='uri')

    # TODO: Add validator DOIs.
    @validates('raw')
    def valid_uri(self, key, uri):
        pattern = re.compile('10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)
        assert pattern.match(uri)
        return uri
        # FIXME: this only validates DOIs.

    def __str__(self):
        return self.raw

    # TODO
    # @property
    # def owners(self):
    #     return self.users.all()


class Url(Model):
    """Url associated with DOI."""

    __tablename__ = 'url'

    id = Column(Integer, primary_key=True)
    url = Column(String)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)

    @validates('url')
    def url_validator(self, key, url):
        assert url_validator(url)
        return url

    def __str__(self):
        return self.url


class Scrape(Model):
    """Keep track of when DOIs were checked for new events."""

    __tablename__ = 'scrape'

    id = Column(Integer, primary_key=True)

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    # Child Relationships
    errors = relationship('Error', backref='scrape')
    raw_events = relationship('RawEvent', backref='scrape')

    def __str__(self):
        return f'<Scrape on: {self.start_date}>'


class Error(Model):
    """ Keep track of failed scrapes for a given doi and origin. Only created
    when scrape task exceeds max retries.

    Columns:
    --------
    description:
        Description of error.
    last_successful_scrape_at:
        when last successful scrape occurred. Used when looking for new events.
    """

    __tablename__ = 'error'

    id = Column(Integer, primary_key=True)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)
    scrape_id = Column(Integer, ForeignKey('scrape.id'), nullable=False)

    origin = Column(ENUM(Origins), nullable=False)
    provider = Column(ENUM(StaticProviders), nullable=False)
    description = Column(String(100))
    last_successful_scrape_at = Column(DateTime, nullable=False)

    def __str__(self):
        return f'<Error: {self.id} - {self.description}>'


class Event(Model):
    """ Hold data related to the events with unique subject ids.

    Columns:
    --------
    origin:
        The service where the event originated (e.g. Twitter).
    subject_id:
        identifier of the event, e.g. url of a tweet, doi of citing article.
    created_at:
        When this event first occurred on the origin service (specified by
        the provider).
    """

    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)

    subject_id = Column(String, nullable=False)
    origin = Column(ENUM(Origins), nullable=False)
    created_at = Column(DateTime, nullable=False)

    raw_events = relationship('RawEvent', backref='event')

    __table_args__ = (
        UniqueConstraint('uri_id', 'subject_id'),
    )

    def __str__(self):
        return f'<Event: {self.id} - {self.uri}>'


class RawEvent(Model):  # May want to rename this (and the Event table)
    """ Hold raw event data. This may be duplicated for what we would consider
    to be a single 'event'. For example, if a Wikipedia page is updated it
    creates an event on Crossref Event Data, but this should not add to the
    metrics count.

    Columns:
    --------
    provider:
        The service we are talking to in order to retrieve the event
        (e.g. Crossref Event Data API).
    origin:
        The service where the event originated (e.g. Twitter).
    external_id:
        id of the event as specified by the provider (e.g. UUID of Crossref
        Event data event)
    created_at:
        When this event occurred on the origin service (specified by the
        provider).
    """

    __tablename__ = 'raw_event'

    id = Column(Integer, primary_key=True)

    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    scrape_id = Column(Integer, ForeignKey('scrape.id'), nullable=False)

    external_id = Column(String, unique=True, nullable=True)
    origin = Column(ENUM(Origins), nullable=False)
    provider = Column(ENUM(StaticProviders), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __str__(self):
        return f'<Raw Event: {self.id} - {self.uri}>'
        # TODO: Add raw_events to URI table


class DeletedEvent(Model):
    """ Hold data related to the events that have been deleted from their
    source/origin. Kept for historical purposes.
    """

    __tablename__ = 'deleted_event'

    id = Column(Integer, primary_key=True)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)

    subject_id = Column(String, nullable=False)
    origin = Column(ENUM(Origins), nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('uri_id', 'subject_id'),
    )

    def __str__(self):
        return f'<Deleted Event: {self.id} - {self.uri}>'


class Metric(Model):
    """Sum of events for a given doi for each origin."""

    __tablename__ = 'metric'

    id = Column(Integer, primary_key=True)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)

    data = Column(HSTORE)
    last_updated = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'<Metric: {self.uri}: {self.data}>'
