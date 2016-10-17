import datetime
import pytest
import rest_framework.test
import calorie_counter


@pytest.fixture
def models():
    return calorie_counter.models


@pytest.fixture
def api_client():
    return rest_framework.test.APIClient()


@pytest.fixture
@pytest.mark.django_db
def user(django_user_model):
    return django_user_model.objects.create_user(
            username='some_user', is_staff=False, is_superuser=False)


@pytest.fixture
@pytest.mark.django_db
def user_with_meal(user, django_user_model, models):
    meal = models.Meal.objects.create(
        text='hearty meal',
        time=datetime.time(),
        date=datetime.date.today(),
        calories=200,
        user=user)
    return (user, meal)
