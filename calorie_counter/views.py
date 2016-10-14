from django.shortcuts import render
from django.contrib.auth.models import User
from calorie_counter.models import Meal
from calorie_counter.serializers import MealSerializer, CreateUserSerializer
from rest_framework import generics, permissions


def index(request):
    return render(request, 'calorie_counter/index.html', {})


class UserPermissions(permissions.BasePermission):
    """
    Users can view their own user object.
    Everything else requires superuser permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        safe_methods = set(permissions.SAFE_METHODS) | {'POST'}
        if request.method not in safe_methods:
            return request.user and request.user.is_superuser
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Use should be authenticated by this point
        return request.user.is_superuser or request.user == obj


class UserList(generics.ListCreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (UserPermissions,)

    def get_queryset(self):
        # Assuming user is authenticated
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.id)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (UserPermissions,)


class MealPermissions(permissions.BasePermission):
    """
    Users can CRUD their own meals.
    Staff can CRUD everybody's meals.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Use should be authenticated by this point
        return request.user.is_staff or request.user == obj.user


class MealList(generics.ListCreateAPIView):
    serializer_class = MealSerializer
    permission_classes = (MealPermissions,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Meal.objects.all()
        else:
            return Meal.objects.filter(user=user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (MealPermissions,)
