import factory

from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
