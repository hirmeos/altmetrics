from django.db import models


class Measure(models.Model):

    namespace = models.ForeignKey(
        'processor.Namespace',
        null=False,
        on_delete=models.PROTECT,
    )
    source = models.ForeignKey(
        'processor.Source',
        null=False,
        on_delete=models.PROTECT,
    )
    type = models.ForeignKey(
        'processor.Type',
        null=False,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return 'Measure {t} for ns: {n}'.format(
            t=self.type,
            n=self.namespace,
        )
