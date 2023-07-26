from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("log", views.log, name="log")
]

