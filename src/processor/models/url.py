from django.db import models

from processor.models import Uri


class Url(models.Model):

    url = models.URLField()
    uri = models.ForeignKey(
        Uri,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.url

    def owners(self):
        return self.uri.owners()
