from django.db import models


class Source(models.Model):

    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return 'Source: {}'.format(self.name)
