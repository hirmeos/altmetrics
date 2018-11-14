from datetime import datetime
from enum import Enum
import re

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.orm import validates
from validators import url as url_validator

from app import app


db = SQLAlchemy(app)


class Origins(Enum):
    twitter_doi = 1
    twitter_url = 2
    wikipedia = 3
    hypothesis = 4
    facebook = 5
    wordpress = 6


class Uri(db.Model):
    """DOI to be scraped."""

    __tablename__ = 'uri'

    id = db.Column(db.Integer, primary_key=True)
    raw = db.Column(db.String(50), unique=True, nullable=False)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)

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


class Url(db.Model):
    """Url associated with DOI."""

    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    uri = db.Column(db.Integer, db.ForeignKey('uri.id'), nullable=False)

    @validates('url')
    def url_validator(self, key, url):
        assert url_validator(url)
        return url

    def __str__(self):
        return self.url


class Scrape(db.Model):
    """Keep track of when DOIs were checked for new events."""

    __tablename__ = 'scrape'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    def __str__(self):
        return f'<Scrape on: {self.start_date}>'


class Error(db.Model):
    """ Keep track of failed scrapes for a given doi and origin. Only created
    when scrape task exceeds max retries.
    """

    __tablename__ = 'error'

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.Integer, db.ForeignKey('uri.id'), nullable=False)
    scrape = db.Column(db.Integer, db.ForeignKey('scrape.id'), nullable=False)
    origin = db.Column(db.String(3))
    description = db.Column(db.String(100))

    def __str__(self):
        return f'<Error: {self.id} - {self.description}>'


class Event(db.Model):
    """ Hold data related to the events.

    A quick note on terminology:

    provider: the service we are talking to in order to retrieve the event
      (e.g. Crossref Event Data API).

    origin: the service where the event originated (e.g. Twitter).
    """

    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.Integer, db.ForeignKey('uri.id'), nullable=False)
    external_id = db.Column(UUID, unique=True, nullable=False)
    origin = db.Enum(Origins)
    created_at = db.Column(db.DateTime)
    scrape = db.Column(db.Integer, db.ForeignKey('scrape.id'), nullable=False)

    def __str__(self):
        return f'<Event: {self.id} - {self.uri}>'


class DeletedEvent(db.Model):
    """ Hold data related to the events that have been deleted from their
    source/origin. Kept for historical purposes.
    """

    __tablename__ = 'deleted_event'

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.Integer, db.ForeignKey('uri.id'), nullable=False)
    external_id = db.Column(UUID, unique=True, nullable=False)
    origin = db.Enum(Origins)
    created_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    scrape = db.Column(db.Integer, db.ForeignKey('scrape.id'), nullable=False)

    def __str__(self):
        return f'<Deleted Event: {self.id} - {self.uri}>'


class Metric(db.Model):
    """Sum of events for a given doi for each origin."""

    __tablename__ = 'metric'

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.Integer, db.ForeignKey('uri.id'), nullable=False)
    data = db.Column(HSTORE)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'<Metric: {self.uri}: {self.data}>'
