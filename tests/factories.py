import random

import pytest
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory


from base.models import Product, Counterparty, NetworkNode
from users.models import User

from datetime import time


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Faker('email')
    phone = Faker('pyint', min_value=79000000000, max_value=79159999999)
    country = Faker('country')
    last_name = Faker('last_name')
    password = Faker('password')
    telegram_username = Faker('pyint', min_value=10000000, max_value=99999999)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker('word')
    release_date = Faker('date')
    model = Faker('word')
    created_at = Faker('date_time')

class CounterpartyFactory(DjangoModelFactory):
    class Meta:
        model = Counterparty

    name = Faker('word')
    email = Faker('email')
    country = Faker('country')
    city = Faker('city')
    street = Faker('word')
    house_number = Faker('pyint', min_value=1, max_value=277)


class NetworkNodeFactory(DjangoModelFactory):
    class Meta:
        model = NetworkNode

    name = Faker('word')
    #node_type = Faker('pyint', min_value=0, max_value=2)
    node_type = 0
    contacts = SubFactory(CounterpartyFactory)
    # products = (SubFactory(ProductFactory),)
    supplier_link = None
    debt = 0.0

    @post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, do nothing.
            return
        self.products.add(*extracted)


    # time_for_action = time(00, random.randint(0, 1), random.randint(0, 59))
    # creator = SubFactory(UserFactory)
    #
    # city = Faker('city')
    # release_date = Faker('date')
    # model = Faker('word')
    # frequency = Faker('pyint', min_value=1, max_value=7)
    # is_public = True
    # is_useful = True