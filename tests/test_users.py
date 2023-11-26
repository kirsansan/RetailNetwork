import pytest
from django.test import Client


# from tests.conftest import token_for_user

@pytest.mark.django_db
class TestUserCreateAndAuth:
    def test_user_create(self):
        """Test user create"""
        client = Client()
        response = client.post(
            '/users/',
            {'email': 'tompson@london.uk', 'password': '12345'},
            content_type='application/json',
        )
        expected_response = {
            'last_login': None,
            'is_superuser': False,
            'first_name': '',
            'is_staff': False,
            'is_active': True,
            'email': 'tompson@london.uk',
            'phone': None,
            'country': None,
            'avatar': None,
            'last_name': None,
            'telegram_username': None,
            'groups': [],
            'user_permissions': []}
        assert response.status_code == 201
        response.data.pop('password')  # it doesn't matter
        response.data.pop('date_joined')  # and it to
        response.data.pop('id')  # might be different with massive tests
        # print("DATA=", response.data)
        assert response.data['email'] == expected_response['email']

    def test_get_users(self, client, token):
        response = client.get(
            '/users/',
            HTTP_AUTHORIZATION="Bearer " + token
        )
        assert response.status_code == 200
        assert response.data[0]['email'] == 'testuser@example.com'


@pytest.mark.django_db
class TestUserDetailUpdate:

    def test_get_one_user(self, authenticated_user: dict):
        user = authenticated_user.get('user')
        client = authenticated_user.get('client')

        # Check retrieve (get)
        response = client.get(f'/users/{user.pk}/')
        assert response.status_code == 200
        # expected_response = {'id': user.pk}
        # print(response.data)
        # assert response.data == expected_response
        assert response.data['email'] == user.email

        # Check update (put)
        new_user_data = {'email': user.email,
                         'last_name': 'NEW lastname'}
        response = client.put(f'/users/{user.pk}/',
                              data=new_user_data)
        assert response.status_code == 200
        assert response.data['last_name'] == 'NEW lastname'

        # Check update (put) with new email
        new_user_data = {'email': 'wrong@email.com',
                         'last_name': 'NEW lastname 2'}
        response = client.put(f'/users/{user.pk}/',
                              data=new_user_data)
        assert response.status_code == 200
        assert response.data['email'] == 'wrong@email.com'
        assert response.data['last_name'] == 'NEW lastname 2'


@pytest.mark.django_db
class TestUserDetailUpdateDeleteAnonymous:

    def test_user_anonymous(self, client, user):
        """Check that anonymous doesn't rigts for anything"""
        response = client.get(f'/users/{user.pk}/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Учетные данные не были предоставлены.'

        new_user_data = {'email': 'wrong@email.com',
                         'last_name': 'NEW lastname 2'}
        response = client.put(f'/users/{user.pk}/', data=new_user_data)
        assert response.status_code == 401
        assert response.data['detail'] == 'Учетные данные не были предоставлены.'

        response = client.delete(f'/users/{user.pk}/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Учетные данные не были предоставлены.'

        response = client.get('/users/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Учетные данные не были предоставлены.'


@pytest.mark.django_db
class TestUserDetailWrongUpdate:

    def test_get_one_user(self, authenticated_user: dict, user):
        auth_user = authenticated_user.get('user')
        auth_client = authenticated_user.get('client')

        # Check update (put) with duplicate email
        new_user_data = {
            'email': user.email,  # try to put non-uniq email
            'last_name': 'some lastname'}
        response = auth_client.put(f'/users/{auth_user.pk}/', data=new_user_data)

        assert response.status_code == 400
        assert str(
            response.data['email']) == "[ErrorDetail(string='user с таким email уже существует.', code='unique')]"

        # Check update someone else's user information
        response = auth_client.put(f'/users/{user.pk}/',
                                   data=new_user_data)
        assert response.status_code == 403
        assert str(response.data['detail']) == "You might see only self-information"


@pytest.mark.django_db
class TestOtherUserInfo:

    def test_other_user_detail(self, authenticated_user: dict, user):
        auth_user = authenticated_user.get('user')
        auth_client = authenticated_user.get('client')

        # Check retrieve (get)
        response = auth_client.get(f'/users/{user.pk}/')
        expected_response = {'pk': user.pk,
                             'email': user.email,
                             'phone': str(user.phone),
                             'country': user.country,
                             'avatar': None,
                             'last_name': user.last_name,
                             'telegram_username': str(user.telegram_username)}
        assert response.status_code == 200
        assert response.data == expected_response

        # Check update (put) with duplicate email and for other user the same time
        new_user_data = {
            'email': auth_user.email,  # try to put for other user
            'last_name': 'some lastname'}
        response = auth_client.put(f'/users/{user.pk}/', data=new_user_data)
        assert response.status_code == 403
        assert str(response.data['detail']) == "You might see only self-information"


# @pytest.mark.django_db
# def test_factories(random_habit, user):
#     print("user:", user)
#     print("habit:", random_habit)
