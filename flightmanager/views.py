from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
from django.db import transaction

import logging

logger = logging.getLogger(__name__)

from .models import Flight, Passanger, Ticket
from django.utils.dateparse import parse_date
from datetime import datetime
# Get an instance of a logger

def index(request):
    flights = Flight.objects
    date_from = request.GET.getlist('date_from')
    date_to = request.GET.getlist('date_to')

    if date_from:
        try:
            flights = flights.filter(start_date__gte=datetime.strptime(date_from[0], '%Y-%m-%d'))
        except (ValueError):
            pass

    if date_to:
        try:
            flights = flights.filter(start_date__lte=datetime.strptime(date_to[0], '%Y-%m-%d'))
        except (ValueError):
            pass

    return render(request, 'flightmanager/index.html', {'flights': flights.all(), 'date_from': date_from, 'date_to': date_to})

def flight_details(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    free_seats = flight.airplane.seat_number - flight.ticket_set.count()
    tickets = flight.ticket_set.all()
    return render(request, 'flightmanager/flight_details.html', {'flight': flight, 'free_seats': free_seats, 'ticekts': tickets})

def add_passanger_form(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    passangers = Passanger.objects.all()
    return render(request, 'flightmanager/add_passanger.html', {'flight': flight, 'passangers': passangers})

def no_tickets(request):
    return render(request, 'flightmanager/no_tickets.html')

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
        new_ticket = Ticket(flight_id=flight_id, passanger=passanger, luggage_weight=luggage_weight)
        new_ticket.save()
        return HttpResponseRedirect(reverse('flightmanager:flight_details', args=(flight_id,)))





