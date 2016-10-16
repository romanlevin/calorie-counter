from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token
from calorie_counter.models import Meal
from calorie_counter.serializers import MealSerializer, CreateUserSerializer
from rest_framework import generics, permissions, exceptions


@requires_csrf_token
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


def str_to_date(date_str):
    import datetime
    if not date_str:
        return None
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def str_to_time(time_str):
    import datetime
    if not time_str:
        return None
    return datetime.datetime.strptime(time_str, '%H:%M').time()


class MealList(generics.ListCreateAPIView):
    serializer_class = MealSerializer
    permission_classes = (MealPermissions,)
    filter_fields = ('calories',)

    def get_date_range(self):
        max_date_str = self.request.GET.get('max_date')
        min_date_str = self.request.GET.get('min_date')
        max_date = str_to_date(max_date_str)
        min_date = str_to_date(min_date_str)
        return (min_date, max_date)

    def get_time_range(self):
        max_time_str = self.request.GET.get('max_time')
        min_time_str = self.request.GET.get('min_time')
        max_time = str_to_time(max_time_str)
        min_time = str_to_time(min_time_str)
        return (min_time, max_time)

    def apply_filters(self, q):
        min_date, max_date = self.get_date_range()
        if max_date:
            q = q.filter(date__lte=max_date)
        if min_date:
            q = q.filter(date__gte=min_date)

        min_time, max_time = self.get_time_range()
        if max_time:
            q = q.filter(time__lte=max_time)
        if min_time:
            q = q.filter(time__gte=min_time)

        return q

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            q = Meal.objects.all()
        else:
            q = Meal.objects.filter(user=user.id)
        return self.apply_filters(q)

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
