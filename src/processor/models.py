from datetime import datetime
import re

from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import validates

from validators import url as url_validator

from core.database import (
    relationship,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Model,
    String,
)


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
    raw = Column(String, unique=True, nullable=False)
    last_checked = Column(DateTime)

    # Child Relationships
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

    @property
    def owners(self):
        return self.users.all()


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

    origin = Column(Integer, nullable=False)
    provider = Column(Integer, nullable=False)
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
    origin = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, default=False)

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
    metrics count. This will also store data related to event deletions.

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
    reason_for_deletion:
        Description of why the event was deleted (applies only to RawEvent
        entries that mark an Event deletion).
    """

    __tablename__ = 'raw_event'

    id = Column(Integer, primary_key=True)

    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    scrape_id = Column(Integer, ForeignKey('scrape.id'), nullable=True)

    external_id = Column(String, unique=True, nullable=True)
    origin = Column(Integer, nullable=False)
    provider = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    reason_for_deletion = Column(String, nullable=True)

    def __str__(self):
        return f'<Raw Event: {self.id} - {self.event.uri}>'


class Metric(Model):
    """Sum of events for a given doi for each origin."""

    __tablename__ = 'metric'

    id = Column(Integer, primary_key=True)

    uri_id = Column(Integer, ForeignKey('uri.id'), nullable=False)

    data = Column(HSTORE)
    last_updated = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'<Metric: {self.uri}: {self.data}>'
