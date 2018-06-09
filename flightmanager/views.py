from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

from django.core import serializers
# Create your views here.
from django.http import HttpResponse
from django.db import transaction

from .models import Flight, Passanger, Ticket, Crew, CrewMember
from datetime import datetime, timedelta

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
    return render(request, 'flightmanager/add_passanger.html', {'flight': flight, 'passangers': passangers, 'validation_error': False})

def no_tickets(request):
    return render(request, 'flightmanager/no_tickets.html')

@login_required
@transaction.atomic
def add_passanger(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    passanger_id = request.POST['select']
    passanger = get_object_or_404(Passanger, pk=passanger_id)
    luggage_weight = request.POST['luggage_weight']
    new_ticket = Ticket(flight_id=flight_id, passenger=passanger, luggage_weight=luggage_weight)

    try:
        new_ticket.full_clean()
    except ValidationError as e:
        passangers = Passanger.objects.all()
        context = {'flight': flight, 'passangers': passangers, 'validation_error': True, 'errors': e.messages}
        return render(request, 'flightmanager/add_passanger.html', context)

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

@require_POST
@csrf_exempt
def do_ajax_login(request):
    if 'username' not in request.POST or 'password' not in request.POST:
        raise PermissionDenied

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        return HttpResponse()
    else:
        return HttpResponseForbidden()

@csrf_exempt
def get_crews(request):
    crews = Crew.objects.prefetch_related('crewmember_set').all()
    crews_parsed = []
    for crew in crews:
        crews_parsed.append({
            'id': crew.id,
            'captain_name': crew.captain_name,
            'captain_surname': crew.captain_surname,
            'members': list(crew.crewmember_set.values('name', 'surname'))})

    return JsonResponse({'crews': list(crews_parsed)})

@require_POST
@csrf_exempt
def add_crew(request):
    if 'username' not in request.POST or 'password' not in request.POST:
        raise PermissionDenied

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is None:
        raise PermissionDenied

    crew = Crew(captain_name=request.POST['captainName'], captain_surname=request.POST['captainSurname'])

    try:
        crew.full_clean()
    except ValidationError as e:
        parssed = ""
        for message in e.messages:
            parssed = parssed + " " + message

        return HttpResponseForbidden(parssed)

    crew.save()

    for member_json in request.POST.getlist('members[]'):
        member = json.loads(member_json)
        if 'name' in member and 'surname' in member:
            CrewMember(name=member['name'], surname=member['surname'], crew=crew).save()

    return HttpResponse()

@csrf_exempt
def get_assignments(request):
    flights = Flight.objects
    date = request.GET.getlist('date')

    if date:
        try:
            parsed_date = datetime.strptime(date[0], '%Y-%m-%d')
            end_date = parsed_date + timedelta(days=1)
            flights = flights.filter(departure_date__gte=parsed_date).filter(departure_date__lte=end_date)
        except (ValueError):
            pass


    flights = flights.select_related('crew').prefetch_related('crew__crewmember_set').all()
    flights_parsed = []
    for flight in flights:
        if flight.crew:
            flights_parsed.append({
                'id': flight.id,
                'from': flight.departure_airport,
                'to': flight.arrival_airport,
                'crew': {
                    'captain_name': flight.crew.captain_name,
                    'captain_surname': flight.crew.captain_surname,
                    'members': list(flight.crew.crewmember_set.values('name', 'surname'))
                }
            })
        else:
            flights_parsed.append({
                'id': flight.id,
                'from': flight.departure_airport,
                'to': flight.arrival_airport
            })

    return JsonResponse({'flights': list(flights_parsed)})

@csrf_exempt
def assign(request):
    if 'username' not in request.POST or 'password' not in request.POST or \
            'flightId' not in request.POST or 'crewId' not in request.POST:
        raise PermissionDenied

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is None:
        raise PermissionDenied

    flight_id = request.POST['flightId']
    crew_id = request.POST['crewId']
    flight = get_object_or_404(Flight, pk=flight_id)
    crew = get_object_or_404(Crew, pk=crew_id)

    flight.crew = crew

    try:
        flight.full_clean()
    except ValidationError as e:
        parssed = ""
        for message in e.messages:
            parssed = parssed + " " + message

        return HttpResponseForbidden(parssed)

    flight.save()

    return HttpResponse()