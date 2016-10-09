from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    text = models.TextField()
    calories = models.PositiveSmallIntegerField()
    time = models.TimeField()
    date = models.DateField()
    user = models.ForeignKey('auth.User', related_name='meals')

    class Meta:
        ordering = ('date', 'time')


class CalorieLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='calorie_limit')
    calorie_limit = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%d' % self.calorie_limit
