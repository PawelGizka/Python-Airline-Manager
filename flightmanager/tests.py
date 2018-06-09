from django.test import TestCase
from django.contrib.auth.models import User
from flightmanager.models import Airplane, Flight, Passanger, Ticket, Crew, CrewMember
from datetime import datetime, timedelta
from django.utils import timezone
# Create your tests here.

import logging
logger = logging.getLogger(__name__)

class CrewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='sans', password='sans')

        airplane1 = Airplane(registration_number="SP-A", seat_number=20)
        airplane1.full_clean()
        airplane1.save()

        airplane2 = Airplane(registration_number="SP-B", seat_number=20)
        airplane2.full_clean()
        airplane2.save()

        crew = Crew(captain_name="John", captain_surname="Smith")
        crew.full_clean()
        crew.save()

        departure_date = timezone.now()
        arrival_date = departure_date + timedelta(hours=5)


        #fligh1 and flight2 in the same time
        flight1 = Flight(departure_date=departure_date, arrival_date=arrival_date,
                        departure_airport="Warsaw", arrival_airport="Rzeszow",
                        airplane=airplane1, crew=crew)

        flight1.full_clean()
        flight1.save()

        flight2 = Flight(departure_date=departure_date, arrival_date=arrival_date,
                         departure_airport="London", arrival_airport="Lublin",
                         airplane=airplane2) #without crew

        flight2.full_clean()
        flight2.save()

        flight3 = Flight(departure_date=departure_date + timedelta(days=2), arrival_date=arrival_date + timedelta(days=3),
                         departure_airport="Warsaw", arrival_airport="Rzeszow",
                         airplane=airplane2)  # without crew

        flight3.full_clean()
        flight3.save()


    def testListingAssignments(self):
        response = self.client.get('/airlinemanager/ajax/get_assignments/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {"flights": [
                                 {"id": 1, "from": "Warsaw", "to": "Rzeszow", "crew": {"captain_name": "John", "captain_surname": "Smith", "members": []}},
                                 {"id": 2, "from": "London", "to": "Lublin"},
                                 {"id": 3, "from": "Warsaw", "to": "Rzeszow"}
                             ]})

    def testMakingAssignmentPositive(self):
        self.assertIsNone(Flight.objects.get(pk=3).crew)
        response = self.client.post('/airlinemanager/ajax/assign/',
                                    data={'username': 'sans', 'password': 'sans', 'crewId': 1, 'flightId': 3,})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Flight.objects.get(pk=3).crew)

    def testMakingAssignmentNegative(self):
        self.assertIsNone(Flight.objects.get(pk=2).crew)
        response = self.client.post('/airlinemanager/ajax/assign/',
                                    data={'username': 'sans', 'password': 'sans', 'crewId': 1, 'flightId': 2,})
        self.assertEqual(response.status_code, 403)
        self.assertIsNone(Flight.objects.get(pk=2).crew)
