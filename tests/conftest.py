import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from tests.factories import UserFactory, ProductFactory, CounterpartyFactory, NetworkNodeFactory

# Factories

register(UserFactory)


@pytest.fixture()
@pytest.mark.django_db
def token(client, django_user_model):
    email = "testuser@example.com"
    password = "12345"
    last_name = "testuser"
    telegram_username = "11122233344"

    django_user_model.objects.create_user(
        email=email, password=password, last_name=last_name, telegram_username=telegram_username
    )

    response = client.post(
        "/users/token/",
        {"email": email, "password": password},
        format='json'
    )

    return response.data["access"]


# def token_for_user(my_client: Client, my_user):
#     """Returns access token for my_user"""
#     print("UWEEE:", my_user.email)
#     www_user = User.objects.get(pk=my_user.pk)
#     print("www_user:", www_user, "password", my_user.password)
#     response = my_client.post(
#         "/users/token/",
#         {"email": my_user.email, "password": my_user.password},
#         format='json'
#     )
#     print("response:", response.status_code)
#     return response.data["access"]


@pytest.fixture
def user():
    user = UserFactory()
    user.set_password("12345")
    return user


@pytest.fixture
@pytest.mark.django_db
def authenticated_user():
    user = UserFactory.create()
    password = user.password
    user.set_password(password)
    user.save()
    # create_instances_for_user(user)
    client = APIClient()
    # client.login(email=user.email, password=password)
    client.force_authenticate(user=user)
    return {'client': client, 'user': user, 'password': password}


@pytest.fixture
@pytest.mark.django_db
def non_active_user():
    user = UserFactory.create()
    password = user.password
    user.set_password(password)
    user.is_active = False
    user.save()
    # create_instances_for_user(user)
    client = APIClient()
    # client.login(email=user.email, password=password)
    client.force_authenticate(user=user)
    return {'client': client, 'user': user, 'password': password}

# @pytest.fixture
# def base_habit():
#     new_data = {"title": "TITLE",
#                 "place": "home_sweet_home",
#                 "time": "12:52:00",
#                 "action": "swim to the test",
#                 "associated_habit": None,
#                 "time_for_action": "0:01:14",
#                 "frequency": 3,
#                 "is_useful": False,
#                 "is_public": False}
#     return new_data


# @pytest.fixture(autouse=True)
# def reset_db_before_test():
#     # Вызывает db.reset_db() перед каждым тестом
#     db.reset_db()

@pytest.fixture
def random_product():
    pr = ProductFactory()
    return pr


@pytest.fixture
def random_contact():
    ct = CounterpartyFactory()
    return ct



@pytest.fixture
def node_f_maker():
    f = NetworkNodeFactory()
    return f
