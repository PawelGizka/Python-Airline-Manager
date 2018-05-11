from django.core.management.base import BaseCommand, CommandError
from flightmanager.models import Airplane, Flight, Passanger, Ticket
from datetime import datetime, timedelta
from django.utils import timezone
from random import randint

class Command(BaseCommand):
    help = 'Generates sample data'

    def handle(self, *args, **options):
        passenger_ids = []

        for i in range(100):
            passenger = Passanger(name="John-" + str(i), surname="Smith-" + str(i))
            passenger.full_clean()
            passenger.save()
            passenger_ids.append(passenger.pk)


        airports = ['Warsaw', 'Lublin', 'Rzeszow', 'Gdansk',
                    'Krakow', 'Wroclaw', 'Szczecin', 'Berlin',
                    'Paris', 'Barcelona', 'Budapeszt', 'Praga']

        #generate 50 airplanes
        for airplane_num in range(50):
            seat_number = 20 + airplane_num*4
            airplane = Airplane(registration_number="SP-A" + str(airplane_num), seat_number=seat_number)
            airplane.full_clean()
            airplane.save()

            #generate 50 flights per airplane
            for flight_num in range(50):
                departure_date = timezone.now() + timedelta(days=flight_num)
                arrival_date = departure_date + timedelta(hours=5)

                departure_index = randint(0, len(airports) - 1)
                arrival_index = randint(0, len(airports) - 1)
                if departure_index == arrival_index:
                    arrival_index = (departure_index + 1) % len(airports)

                flight = Flight(departure_date=departure_date, arrival_date=arrival_date,
                                departure_airport=airports[departure_index], arrival_airport=airports[arrival_index],
                                airplane=airplane)

                flight.full_clean()
                flight.save()

                #generate 5 tickets per flight
                for ticket_number in range(5):
                    ticket = Ticket(flight=flight,
                                    passenger_id=passenger_ids[randint(0, len(passenger_ids) - 1)],
                                    luggage_weight=randint(0, 30))
                    ticket.full_clean()
                    ticket.save()

            self.stdout.write("generated data for aircraft number " + str(airplane_num))

