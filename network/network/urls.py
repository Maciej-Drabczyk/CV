
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("profile/<str:name>", views.profile, name="profile"),
    path('follow_toggle', views.follow_toggle, name="follow_toggle"),
    path("following", views.following, name="following"),
    path("new_post", views.new_post, name="new_post"),
    path("like_toggle", views.like_toggle, name="like_toggle"),
    path("edit", views.edit, name="edit")
]
