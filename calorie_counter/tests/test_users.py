import pytest


@pytest.mark.django_db
def test_list_users(client):
    response = client.get('/api/users/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_users_as_admin(client):
    response = client.get('/api/users/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_as_admin(client, django_user_model):
    response = client.post(
        '/api/users/',
        {'username': 'admin',
         'password': 'foo123bar',
         'calorie_limit': 100})
    assert response.status_code == 201
    new_user = django_user_model.objects.all()[1]
    assert new_user.username == 'admin'
    assert new_user.calorie_limit.calorie_limit == 100
    response = client.get('/api/users/')
    new_user = response.json()[1]
    new_user['calorie_limit'] == 100
