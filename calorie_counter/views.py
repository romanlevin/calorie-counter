from django.shortcuts import render
from django.contrib.auth.models import User
from calorie_counter.models import Meal
from calorie_counter.serializers import MealSerializer, CreateUserSerializer
from rest_framework import generics, permissions, exceptions


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


class UserMealList(generics.ListAPIView):
    serializer_class = MealSerializer
    permission_classes = (MealPermissions,)
    lookup_field = 'user'

    def get_queryset(self):
        lookup_user_id = self.kwargs['user']
        if not User.objects.filter(pk=lookup_user_id):
            # Lookup user does not exist
            raise exceptions.NotFound()
        user = self.request.user
        if user.is_staff or user.id == lookup_user_id:
            return Meal.objects.all(user=lookup_user_id)
        else:
            # Not authorised to view this user's meals
            raise exceptions.NotFound()
