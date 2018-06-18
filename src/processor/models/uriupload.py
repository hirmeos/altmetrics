from django.db import models


class UriUpload(models.Model):

    uri = models.ForeignKey(
        'processor.Uri',
        null=False,
        on_delete=models.PROTECT
    )
    upload = models.ForeignKey(
        'importer.CSVUpload',
        null=False,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return 'DoiUpload: {}, {}'.format(self.uri, self.upload)

    def owner(self):
        return self.upload.user
