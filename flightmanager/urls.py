from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flights/<int:flight_id>', views.flight_details, name='flight_details'),
]