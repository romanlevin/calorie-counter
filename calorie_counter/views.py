from django.http import HttpResponse
from django.contrib.auth.models import User
from calorie_counter.models import Meal
from calorie_counter.serializers import MealSerializer, CreateUserSerializer
from rest_framework import generics


def index(request):
    return HttpResponse('Hello, world. This is the calorie_counter index')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
