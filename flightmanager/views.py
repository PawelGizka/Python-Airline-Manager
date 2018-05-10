from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse

from .models import Flight

def index(request):
    all_flights = Flight.objects.all()
    return render(request, 'flightmanager/index.html', {'flights': all_flights})

def flight_details(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    free_seats = flight.airplane.seat_number - flight.ticket_set.count()
    tickets = flight.ticket_set.all()
    return render(request, 'flightmanager/flight_details.html', {'flight': flight, 'free_seats': free_seats, 'ticekts': tickets})

