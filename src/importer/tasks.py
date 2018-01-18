from csv import reader as csv_reader
from io import StringIO

from core.celery import app
from processor.models import Doi


@app.task(name='register-dois')
def register_doi(csv, upload_id):
    """ Given a CSV model object, get csv and register the DOIs in the database.

    Args:
        csv (str): A string representing the content of a CSV.
        upload_id (int): ID of the CSVUpload from last import for this DOI.
    """

    reader = csv_reader(StringIO(csv))

    for row in reader:
        Doi.objects.create(
            doi=row[0].strip(' '),
            last_upload_id=upload_id,
        )
