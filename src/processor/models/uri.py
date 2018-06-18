# from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models


class Uri(models.Model):

    raw = models.CharField(
        max_length=50,
        unique=True,
        # validators=[
        #     RegexValidator(  # FIXME: this only validates DOIs.
        #         regex='/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i',
        #         message='DOI not valid.',
        #     ),
        # ],
    )
    last_checked = models.DateTimeField(
        null=True,
        default=None,
    )
    uploader = models.ForeignKey(
        User,
        null=True,
        unique=False,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.raw

    @property
    def owner(self):
        return self.uploader or [
            uri_upload.owner() for uri_upload in self.uriupload_set.all()
        ]
