import pytest
from calorie_counter.models import CalorieLimit


@pytest.mark.django_db
def test_list_users(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_list_users_as_admin(admin_client):
    response = admin_client.get('/api/users/')
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_create_user_as_admin(admin_client, django_user_model):
    response = admin_client.post(
        '/api/users/',
        {'username': 'frodo',
         'password': 'foo123bar',
         'calorie_limit': 100})
    assert response.status_code == 201
    new_user_id = response.json()['id']
    new_user = django_user_model.objects.get(pk=new_user_id)
    assert new_user.username == 'frodo'
    assert new_user.calorie_limit.calorie_limit == 100


@pytest.mark.django_db
def test_view_user_as_admin(admin_client, django_user_model):
    user = django_user_model.objects.create_user(
        username='user1',
        password='magical',
    )
    CalorieLimit.objects.create(
        user=user,
        calorie_limit=100,
    )
    response = admin_client.get('/api/users/%d/' % user.pk)
    assert response.json()['calorie_limit'] == 100
