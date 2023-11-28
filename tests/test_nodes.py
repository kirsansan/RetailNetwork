import pytest
from config.config import MAX_NODE_PER_PAGE
from base.models import NetworkNode
from tests.factories import NetworkNodeFactory
from users.models import User


@pytest.mark.django_db
def test_get_nodes_list(authenticated_user):
    auth_client = authenticated_user.get('client')
    # NetworkNodeFactory.create()
    [NetworkNodeFactory.create_batch(MAX_NODE_PER_PAGE) for _ in range(0, 7)]
    response = auth_client.get('/nodes/all/')
    assert response.status_code == 200
    assert len(response.data['results']) == MAX_NODE_PER_PAGE


@pytest.mark.django_db
def test_get_nodes_list_diff_users(authenticated_user, non_active_user):
    auth_client = authenticated_user.get('client')
    non_active_client = non_active_user.get('client')
    nodes = NetworkNodeFactory.create_batch(2)  # two default

    # we will see 2 objects  - both nodes for active
    response = auth_client.get('/nodes/all/')
    assert response.status_code == 200
    assert len(response.data['results']) == 2

    # we will not be able to see anything - all nodes are not public
    response = non_active_client.get('/nodes/all/')
    assert response.status_code == 403
    # assert len(response.data['results']) == 2


#
# @pytest.mark.django_db
# def test_get_habit_list_as_creator(authenticated_user):
#     auth_client = authenticated_user.get('client')
#     auth_user: User = authenticated_user.get('user')
#     habits = HabitFactory.create_batch(2)  # two default
#     for habit in habits:  # make both habits like as we are a creator of them
#         habit.creator = auth_user
#         habit.is_public = False
#         habit.save()
#
#     # we will not be able to see anything - all habits are not public
#     response = auth_client.get('/habit/all/')
#     assert response.status_code == 200
#     assert len(response.data['results']) == 0
#
#     # we will see 2 objects  - both habits have 'creator' with our mentions
#     response = auth_client.get('/habit/my/')
#     assert response.status_code == 200
#     assert len(response.data['results']) == 2
#
#
# @pytest.mark.django_db
# def test_get_habit_detail(authenticated_user):
#     auth_client = authenticated_user.get('client')
#     auth_user = authenticated_user.get('user')
#     habits: list[Habit] = HabitFactory.create_batch(3)  # two default
#     tmp_habit = habits[0]
#
#     # check someone else's habit (not mine)
#     response = auth_client.get(f'/habit/detail/{tmp_habit.pk}/')
#     assert response.status_code == 403
#     assert str(response.data['detail']) == "У вас недостаточно прав для выполнения данного действия."
#
#     # make this habit mine
#     tmp_habit.creator = auth_user
#     tmp_habit.save()
#     response = auth_client.get(f'/habit/detail/{tmp_habit.pk}/')
#     expected_response = {'id': tmp_habit.pk,
#                          'title': tmp_habit.title,
#                          'place': tmp_habit.place,
#                          'time': tmp_habit.time,
#                          'action': tmp_habit.action,
#                          'is_useful': tmp_habit.is_useful,
#                          'frequency': tmp_habit.frequency,
#                          'reward': tmp_habit.reward,
#                          'time_for_action': str(tmp_habit.time_for_action),
#                          'is_public': tmp_habit.is_public,
#                          'creator': tmp_habit.creator.pk,
#                          'associated_habit': tmp_habit.associated_habit}
#     assert response.status_code == 200
#     assert response.data == expected_response
#
#
# @pytest.mark.django_db
# def test_create_habit(authenticated_user):
#     auth_client = authenticated_user.get('client')
#     auth_user = authenticated_user.get('user')
#
#     new_data = {"title": "push up",
#                 "place": "home_sweet_home",
#                 "time": "14:52:00",
#                 "action": "jazz up",
#                 "associated_habit": None,
#                 "time_for_action": "0:1:25",
#                 "frequency": 3,
#                 "is_useful": False}
#     response = auth_client.post('/habit/create/', new_data, format='json')
#     assert response.status_code == 201
#     response.data.pop('id')
#     expected_response = {
#         "title": "push up",
#         "place": "home_sweet_home",
#         "time": "14:52:00",
#         "action": "jazz up",
#         "is_useful": False,
#         "associated_habit": None,
#         "time_for_action": "00:01:25",
#         "frequency": 3,
#         "reward": None,
#         "is_public": True,
#         "creator": auth_user.pk
#     }
#     assert response.data == expected_response
#
#
# @pytest.mark.django_db
# def test_delete_habit(authenticated_user):
#     auth_client = authenticated_user.get('client')
#     auth_user = authenticated_user.get('user')
#     habit = HabitFactory(creator=auth_user)
#
#     response = auth_client.delete(f'/habit/delete/{habit.pk}/')
#     assert response.status_code == 204
#
#     # Check that the habit was deleted from the database
#     with pytest.raises(Habit.DoesNotExist):
#         habit.refresh_from_db()
