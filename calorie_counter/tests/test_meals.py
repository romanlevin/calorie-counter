import datetime
import pytest
from calorie_counter import models


@pytest.mark.django_db
def test_list_meals_empty(client):
    response = client.get('/api/meals/')
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.django_db
def test_create_meal(client, django_user_model):
    user = django_user_model.objects.create_user('admin', 'crazypassword')
    meal = models.Meal.objects.create(
        text='hearty meal',
        time=datetime.time(),
        date=datetime.date.today(),
        calories=200,
        user=user)
    response = client.get('/api/meals/%d/' % meal.pk)
    assert response.status_code == 200
