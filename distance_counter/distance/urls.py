from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("log", views.log, name="log"), 
    path("login/", views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("register/", views.register, name="register"),
    path("<int:distance_id>", views.distance, name="distance"),
    path('office/create/', views.office_create, name='office_create'),
    path('log/create/', views.log_create, name='log_create'),
    path('person/create/', views.person_create, name='person_create'),
    path('unit/create/', views.unit_create, name='unit_create')

]

