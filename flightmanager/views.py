from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.core import serializers
# Create your views here.
from django.http import HttpResponse
from django.db import transaction

from .models import Flight, Passanger, Ticket
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

def index(request):
    flights = Flight.objects
    date_from = request.GET.getlist('date_from')
    date_to = request.GET.getlist('date_to')

    if date_from:
        try:
            flights = flights.filter(departure_date__gte=datetime.strptime(date_from[0], '%Y-%m-%d'))
        except (ValueError):
            pass

    if date_to:
        try:
            flights = flights.filter(departure_date__lte=datetime.strptime(date_to[0], '%Y-%m-%d'))
        except (ValueError):
            pass

    context = {'flights': flights.all(), 'is_user_authenticated': request.user.is_authenticated,
               'date_from': date_from, 'date_to': date_to}

    return render(request, 'flightmanager/index.html', context)

@login_required
def flight_details(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    free_seats = flight.airplane.seat_number - flight.ticket_set.count()
    tickets = flight.ticket_set.all()
    context = {'flight': flight, 'is_user_authenticated': request.user.is_authenticated,
               'free_seats': free_seats, 'tickets': tickets}
    return render(request, 'flightmanager/flight_details.html', context)

@login_required
def add_passanger_form(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    passangers = Passanger.objects.all()
    return render(request, 'flightmanager/add_passanger.html', {'flight': flight, 'passangers': passangers})

def no_tickets(request):
    return render(request, 'flightmanager/no_tickets.html')

@login_required
@transaction.atomic
def add_passanger(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    free_seats = flight.airplane.seat_number - flight.ticket_set.count()
    if free_seats == 0:
        return HttpResponseRedirect(reverse('flightmanager:no_tickets'))
    else:
        passanger_id = request.POST['select']
        passanger = get_object_or_404(Passanger, pk=passanger_id)
        luggage_weight = request.POST['luggage_weight']
        new_ticket = Ticket(flight_id=flight_id, passenger=passanger, luggage_weight=luggage_weight)

        try:
            new_ticket.full_clean()
        except ValidationError as e:
            return HttpResponseBadRequest(e.messages)

        new_ticket.save()
        return HttpResponseRedirect(reverse('flightmanager:flight_details', args=(flight_id,)))

def login_form(request):
    next = request.GET.getlist('next')
    return render(request, 'flightmanager/login.html', {'incorrect_login': False, 'next': next})

def incorrect_login_form(request):
    next = request.GET.getlist('next')
    return render(request, 'flightmanager/login.html', {'incorrect_login': True, 'next': next})

def do_login(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next = request.GET.getlist('next')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next[0])
            else:
                return HttpResponseRedirect(reverse('flightmanager:index'))
        else:
            return HttpResponseRedirect(reverse('flightmanager:incorrect_login_form'))

    else:
        return HttpResponseBadRequest("request must contain username and password")



def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('flightmanager:index'))



