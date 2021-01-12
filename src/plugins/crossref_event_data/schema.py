from dateutil.parser import parse as parse_date_string
import re

from marshmallow import fields
from marshmallow.exceptions import ValidationError

from core.settings import Origins
from core.logic import get_enum_by_name
from processor.models import Uri
from processor.schemas import EventSchema


DOI_PATTERN = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)


def determine_doi(doi_string):
    match = DOI_PATTERN.search(doi_string)
    if match:
        return match.group()


class CrossRefEventSchema(EventSchema):
    """ Turn a CrossRefEventData event into an HIRMEOS metrics Event """

    external_id = fields.Method('get_external_id')
    subject_id = fields.Method('get_subject_id')
    created_at = fields.Method('get_datetime_created_at')

    @staticmethod
    def get_subject_id(obj):
        """Some 'subj' sections are incompatible with out source list."""
        subject = obj.get('subj')
        if subject and 'pid' in subject:
            if 'oldid=' in subject['pid']:
                return subject.get('url')
            return subject['pid']

    @staticmethod
    def get_datetime_created_at(obj):
        try:
            return parse_date_string(obj.get('occurred_at'))
        except ValueError:
            raise ValidationError('Not a valid datetime string.')

    def get_origin(self, obj):
        return get_enum_by_name(Origins, obj.get('source_id'))

    @staticmethod
    def get_external_id(obj):
        return obj.get('id')

    def get_uri(self, obj):
        doi_raw = determine_doi(obj.get('obj_id'))
        doi_obj = Uri.query.filter_by(raw=doi_raw).first()
        if doi_obj:
            return doi_obj.id
