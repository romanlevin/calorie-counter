from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/meals/$', views.MealList.as_view()),
    url(r'^api/meals/(?P<pk>[0-9]+)/$', views.MealDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api/users/(?P<user>[0-9]+)/meals/$', views.UserMealList.as_view()),
]
