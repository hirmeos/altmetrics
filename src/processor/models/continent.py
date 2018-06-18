from django.db import models


class Continent(models.Model):

    name = models.DateTimeField()

    def __str__(self):
        return 'Continent: {}'.format(self.name)
