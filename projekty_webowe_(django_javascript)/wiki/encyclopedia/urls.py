from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/", views.entry, name="page"),
    path("search/", views.search, name="search"),
    path("create/", views.create_new, name="create"),
    path("random/", views.random, name="random")
]
