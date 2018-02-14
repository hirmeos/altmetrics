from unicodedata import normalize

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from boto3 import client as s3client

from .tasks import register_doi

class CSVUpload(models.Model):

    file_name = models.CharField(
        max_length=250,
    )
    link = models.URLField(
        max_length=250,
    )
    date_uploaded = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        null=False,
        unique=False,
        on_delete=models.DO_NOTHING,
    )
    processed = models.BooleanField(
        default=False,
    )

    @property
    def content(self):
        client = s3client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        return normalize(
            "NFKD",
            client.get_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=self.file_name,
            )['Body'].read().decode('utf-8')
        )


@receiver(post_save, sender=CSVUpload)
def import_dois(sender, instance, **kwargs):
    """ Trigger a Celery task to save DOIs into database at every CSV upload.

    Args:
        sender (object): Sender.
        instance (CSVUpload): CSV object which has triggered the signal.
    """
    pass
    register_doi.delay(instance.content, instance.id)
