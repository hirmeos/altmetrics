from django.contrib.postgres.fields import ArrayField
from django.db import models


class Namespace(models.Model):

    definition_url = models.URLField(
        null=True,
    )
    allowed_origins = ArrayField(
        models.CharField(max_length=10, blank=True),
        size=8,
    )

    def __str__(self):
        return 'Namespace: {}'.format(self.definition_url)
