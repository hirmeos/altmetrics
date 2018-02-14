from csv import reader as csv_reader
from io import StringIO

from celery.utils.log import get_task_logger
from core.celery import app
from processor.models import Doi, DoiUpload, Url

logger = get_task_logger(__name__)


@app.task(name='register-dois')
def register_doi(csv, csv_upload_id):
    """ Given a CSV model object, get csv and register the DOIs in the database.

    Args:
        csv (str): A string representing the content of a CSV.
        csv_upload_id (int): ID of the CSVUpload from last import for this DOI.
    """
    try:
        with StringIO(csv) as p:
            reader = csv_reader(p)

            for row in reader:
                if (
                    len(row) >= 2 and
                    len(row[0].strip()) > 0
                    and len(row[1].strip()) > 0
                ):
                    doi, _ = Doi.objects.get_or_create(
                        doi=row[1].strip(),
                    )

                    Url.objects.get_or_create(
                        url=row[0].strip(),
                        doi=doi
                    )

                    DoiUpload.objects.get_or_create(
                        doi=doi,
                        upload_id=csv_upload_id
                    )
                else:
                    msg = 'Problem parsing line {line_num} ' \
                          'for csv upload id of {upload_id}'.format(
                              line_num=reader.line_num,
                              upload_id=csv_upload_id,
                          )
                    logger.error(msg)
                    print(msg)
    except Exception as e:
        logger.error(e)
        print(e)
