from django.db import models


class Scrape(models.Model):

    start_date = models.DateTimeField(
        auto_now_add=True,
    )
    end_date = models.DateTimeField(
        null=True,
    )

    def __str__(self):
        return 'Scrape on: {}'.format(self.start_date)
