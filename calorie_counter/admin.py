from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from calorie_counter.models import CalorieLimit


class CalorieLimitInline(admin.StackedInline):
    model = CalorieLimit
    can_delete = False
    verbose_name_plural = 'calorie limit'


class UserAdmin(BaseUserAdmin):
    inlines = (CalorieLimitInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
