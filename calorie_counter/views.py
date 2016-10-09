from django.http import HttpResponse
from django.contrib.auth.models import User
from calorie_counter.models import Meal
from calorie_counter.serializers import MealSerializer, CreateUserSerializer
from rest_framework import generics, permissions
from rest_framework.compat import is_authenticated


def index(request):
    return HttpResponse('Hello, world. This is the calorie_counter index')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class MealPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user)

    def has_object_permission(self, request, view, obj):
        # Use should be authenticated by this point
        return request.user.is_staff or request.user == obj.user


class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (MealPermissions,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (MealPermissions,)
