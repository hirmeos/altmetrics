from datetime import datetime

import re

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.orm import validates
from validators import url as url_validator

from app import app
from core.settings import StaticProviders, Origins


db = SQLAlchemy(app)

# alias common db types
Column = db.Column
DateTime = db.DateTime
Enum = db.Enum
ForeignKey = db.ForeignKey
Integer = db.Integer
Model = db.Model
String = db.String
relationship = db.relationship


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
        pattern = re.compile('10.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)
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
    deleted_events = relationship('DeletedEvent', backref='scrape')
    errors = relationship('Error', backref='scrape')
    events = relationship('Event', backref='scrape')

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

    origin = Enum(Origins, nullable=False)
    provider = Enum(StaticProviders, nullable=False)
    description = Column(String(100))
    last_successful_scrape_at = Column(DateTime, nullable=False)

    def __str__(self):
        return f'<Error: {self.id} - {self.description}>'


class Event(Model):
    """ Hold data related to the events.

    Columns:
    --------
    provider:
        The service we are talking to in order to retrieve the event
        (e.g. Crossref Event Data API).
    origin:
        The service where the event originated (e.g. Twitter).
    external_id:
        id of the event as specified by the provider.
    created_at:
        When this event occured on the origin service (specified by the
        provider).
    """

    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)
    scrape_id = Column(Integer, ForeignKey('scrape.id'), nullable=False)

    external_id = Column(UUID, unique=True, nullable=False)
    origin = Enum(Origins, nullable=False)
    provider = Enum(StaticProviders, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __str__(self):
        return f'<Event: {self.id} - {self.uri}>'


class DeletedEvent(Model):
    """ Hold data related to the events that have been deleted from their
    source/origin. Kept for historical purposes.
    """

    __tablename__ = 'deleted_event'

    id = Column(Integer, primary_key=True)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)
    scrape_id = Column(Integer, ForeignKey('scrape.id'), nullable=False)

    external_id = Column(UUID, unique=True, nullable=False)
    origin = Enum(Origins)
    provider = Enum(StaticProviders)
    created_at = Column(DateTime)
    deleted_at = Column(DateTime)

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
