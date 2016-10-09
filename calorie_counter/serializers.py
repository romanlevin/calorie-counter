from rest_framework import serializers
from calorie_counter.models import Meal, CalorieLimit
from django.contrib.auth.models import User


class MealSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Meal


class CreateUserSerializer(serializers.ModelSerializer):
    calorie_limit = serializers.IntegerField(
        min_value=1,
        required=False,
        allow_null=True,
        source='calorie_limit.calorie_limit')

    class Meta:
        model = User
        fields = ('username', 'password', 'calorie_limit')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])

        user.save()

        print(validated_data)
        calorie_limit = CalorieLimit(
            user=user,
            calorie_limit=validated_data['calorie_limit']['calorie_limit'],
        )

        calorie_limit.save()

        return user
