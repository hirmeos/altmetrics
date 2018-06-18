from django.db import models


class Country(models.Model):

    code = models.CharField(
        max_length=2,
    )
    name = models.CharField(
        max_length=255,
    )
    continent = models.ForeignKey(
        'processor.Continent',
        null=False,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return 'Country: {}'.format(self.name)
