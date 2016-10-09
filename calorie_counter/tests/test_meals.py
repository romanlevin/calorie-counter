import pytest


def test_list_meals_empty(admin_client):
    response = admin_client.get('/api/meals/')
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.django_db
def test_list_meals_not_logged_in(api_client):
    response = api_client.get('/api/meals/')
    assert response.status_code == 403


def test_meal_read(api_client, user_with_meal):
    user, meal = user_with_meal
    response = api_client.get('/api/meals/%d/' % meal.pk)
    assert response.status_code == 403

    api_client.force_login(user)
    response = api_client.get('/api/meals/%d/' % meal.pk)
    assert response.status_code == 200


def test_meal_delete(api_client, user_with_meal):
    user, meal = user_with_meal
    response = api_client.get('/api/meals/%d/' % meal.pk)
    assert response.status_code == 403

    api_client.force_login(user)
    response = api_client.delete('/api/meals/%d/' % meal.pk)
    assert response.status_code == 204


def test_meal_update(api_client, user_with_meal):
    user, meal = user_with_meal
    calories = meal.calories
    more_calories = calories + 100
    response = api_client.patch(
        '/api/meals/%d/' % meal.pk,
        {'calories': more_calories})
    assert response.status_code == 403
    meal.refresh_from_db()
    assert meal.calories == calories

    api_client.force_login(user)
    response = api_client.patch(
        '/api/meals/%d/' % meal.pk,
        {'calories': more_calories})
    assert response.status_code == 200
    meal.refresh_from_db()
    assert meal.calories == more_calories


def test_meal_create(api_client, user, models):
    meal = {
        'text': 'An okay meal',
        'time': '12:32',
        'date': '2013-12-25',
        'calories': 123}
    response = api_client.post('/api/meals/', meal)
    assert response.status_code == 403

    api_client.force_login(user)
    response = api_client.post('/api/meals/', meal)
    assert response.status_code == 201

    meal_object = models.Meal.objects.first()
    assert meal_object.text == meal['text']
