from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = FuzzyText(prefix='first_name_')
    last_name = FuzzyText(prefix='last_name_')
    username = FuzzyText(prefix='username_')
    password = 'test_pass'
