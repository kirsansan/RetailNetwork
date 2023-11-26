import random

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

# from habit.models import Habit
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


# class HabitFactory(DjangoModelFactory):
#     class Meta:
#         model = Habit
#
#     time_for_action = time(00, random.randint(0, 1), random.randint(0, 59))
#     creator = SubFactory(UserFactory)
#     title = Faker('word')
#     place = Faker('city')
#     time = Faker('time')
#     action = Faker('word')
#     frequency = Faker('pyint', min_value=1, max_value=7)
#     is_public = True
#     is_useful = True
