from django.db import models


class Type(models.Model):

    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return 'Measure type: {}'.format(self.name)
