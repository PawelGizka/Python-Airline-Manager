from django.urls import path

from . import views

app_name="flightmanager"
urlpatterns = [
    path('', views.index, name='index'),
    path('flights/<int:flight_id>/', views.flight_details, name='flight_details'),
    path('flights/<int:flight_id>/add_passanger_form/', views.add_passanger_form, name='add_passanger_form'),
    path('flights/<int:flight_id>/add_passanger/', views.add_passanger, name='add_passanger'),
    path('no_tickets/', views.no_tickets, name='no_tickets'),
    path('login_form/', views.login_form, name='login_form'),
    path('incorrect_login_form/', views.incorrect_login_form, name='incorrect_login_form'),
    path('login/', views.do_login, name='login'),
    path('logout/', views.do_logout, name='logout'),
]