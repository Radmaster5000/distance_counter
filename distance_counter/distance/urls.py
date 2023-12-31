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
    path('unit/create/', views.unit_create, name='unit_create'),
    path("<int:distance_id>/edit", views.distance_edit, name="distance_edit"),
    path('<int:distance_id>/delete/', views.delete_distance, name='delete_distance'),
    path("person/<int:person_id>", views.person, name="person"),
    path("people/<int:person_id>/edit/", views.person_edit, name="person_edit"),
    path("people/", views.people, name="people"),
    path('person/<int:person_id>/delete/', views.delete_person, name='delete_person'),
    path("office/<int:office_id>", views.office, name="office"),
    path("offices/<int:office_id>/edit/", views.office_edit, name="office_edit"),
    path("offices/", views.offices, name="offices"),
    path('office/<int:office_id>/delete/', views.delete_office, name='delete_office'),
    path("unit/<int:unit_id>", views.unit, name="unit"),
    path("units/<int:unit_id>/edit/", views.unit_edit, name="unit_edit"),
    path("units/", views.units, name="units"),
    path('unit/<int:unit_id>/delete/', views.delete_unit, name='delete_unit'),
]

