import datetime
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


def test_meal_filters(api_client, user, models):
    meal = {
        'text': 'An okay meal',
        'time': '12:32',
        'date': '2013-12-25',
        'calories': 123}
    api_client.force_login(user)

    response = api_client.post('/api/meals/', meal)
    assert response.status_code == 201

    meal['time'] = '13:00'
    meal['date'] = '2013-12-26'
    response = api_client.post('/api/meals/', meal)
    assert response.status_code == 201

    meal['time'] = '13:10'
    meal['date'] = '2013-12-27'
    response = api_client.post('/api/meals/', meal)
    assert response.status_code == 201

    meal['time'] = '14:10'
    meal['date'] = '2013-12-28'
    response = api_client.post('/api/meals/', meal)
    assert response.status_code == 201

    response = api_client.get('/api/meals/')
    assert len(response.json()) == 4

    response = api_client.get('/api/meals/', {'min_time': '13:00', 'max_time': '13:50'})
    assert len(response.json()) == 2

    response = api_client.get('/api/meals/', {'min_date': '2013-12-27'})
    assert len(response.json()) == 2

    response = api_client.get('/api/meals/', {'max_date': '2014-12-27'})
    assert len(response.json()) == 4


def test_staff_can_list_all_meals(api_client, user, models):
    time = datetime.time(12, 13)
    date = datetime.date(2013, 10, 25)
    meal = models.Meal.objects.create(
        text='A nice salad',
        calories=123,
        time=time,
        date=date,
        user=user
        )
    other_user = models.User.objects.create_user(
        username='staff', password='who cares?', is_staff=False, is_superuser=False)

    response = api_client.get('/api/meals/')
    assert response.status_code == 403

    api_client.force_login(other_user)
    response = api_client.get('/api/meals/')
    meals = response.json()
    assert len(meals) == 0

    other_user.is_staff = True
    other_user.save()
    response = api_client.get('/api/meals/')
    meals = response.json()
    assert len(meals) == 1
    assert meals[0]['id'] == meal.id
