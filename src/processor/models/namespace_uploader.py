from django.db import models

from django.contrib.auth.models import User


class NamespaceUploader(models.Model):

    namespace = models.ForeignKey(
        'processor.Namespace',
        null=False,
        unique=False,
        on_delete=models.DO_NOTHING,
    )
    uploader = models.ForeignKey(
        User,
        null=False,
        unique=False,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return 'Namespace uploader: {}'.format(self.uploader)
