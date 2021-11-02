
from collections import namedtuple
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name='like'),
    path("profile/<str:username>", views.profile, name='profile'),
    path("following", views.following, name="following"),
    path("follow_user/<int:id>", views.follow_user, name="follow_user"),
    path("unfollow_user/<int:id>", views.unfollow_user, name="unfollow_user")
]
