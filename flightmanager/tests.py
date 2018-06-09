from django.test import TestCase
from django.contrib.auth.models import User
from flightmanager.models import Airplane, Flight, Passanger, Ticket, Crew, CrewMember
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# Create your tests here.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
logger = logging.getLogger(__name__)

def mySetup():
    Passanger.objects.create(name='Pawel', surname='Gizka')

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

    # fligh1 and flight2 in the same time
    flight1 = Flight(departure_date=departure_date, arrival_date=arrival_date,
                     departure_airport="Warsaw", arrival_airport="Rzeszow",
                     airplane=airplane1, crew=crew)

    flight1.full_clean()
    flight1.save()

    flight2 = Flight(departure_date=departure_date, arrival_date=arrival_date,
                     departure_airport="London", arrival_airport="Lublin",
                     airplane=airplane2)  # without crew

    flight2.full_clean()
    flight2.save()

    flight3 = Flight(departure_date=departure_date + timedelta(days=2), arrival_date=arrival_date + timedelta(days=3),
                     departure_airport="Warsaw", arrival_airport="Rzeszow",
                     airplane=airplane2)  # without crew

    flight3.full_clean()
    flight3.save()

class CrewTest(TestCase):
    def setUp(self):
        mySetup()

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

WAIT_TIME = 10

class ChatTest(StaticLiveServerTestCase):
    def setUp(self):
        mySetup()

    def testLogin(self):
        h = webdriver.Chrome()
        h.get(self.live_server_url)
        # implicit wait would work
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'login-button')))
        login_button = h.find_element_by_id('login-button')
        self.assertTrue(login_button.is_displayed())
        login_button.click()

        #login screen - check incorrect login info
        h.find_element_by_css_selector('#username').send_keys('sans')
        h.find_element_by_css_selector('#password').send_keys('sans-bad')
        login_button = h.find_element_by_id('login-button')
        self.assertTrue(login_button.is_displayed())
        login_button.click()

        incorrect_login_message = h.find_element_by_id('incorrect_login')
        self.assertTrue(incorrect_login_message.is_displayed())

        #correct login
        h.find_element_by_css_selector('#username').send_keys('sans')
        h.find_element_by_css_selector('#password').send_keys('sans')
        h.find_element_by_id('login-button').click()

        #index
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'logout-button')))
        logout_button = h.find_element_by_id('logout-button')
        self.assertTrue(logout_button.is_displayed())

        #click first flight details button
        h.find_element_by_id('details-1').click()

        #details screen, click add passanger
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'add-passenger-button')))
        h.find_element_by_id('add-passenger-button').click()

        #add passanger screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'add-passenger-button')))
        h.find_element_by_css_selector('#luggage_weight').send_keys('5')
        h.find_element_by_id('add-passenger-button').click()

        #details screen again, check that passanger was added
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'add-passenger-button')))
        passanger_info = h.find_element_by_class_name('passenger-info')
        self.assertTrue(passanger_info.is_displayed())

        #logout
        h.find_element_by_id('logout-button').click()

        #index
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'manage-crews-button')))
        h.find_element_by_id('manage-crews-button').click()

        #go to manage crew - assignments screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'login-button')))
        h.find_element_by_id('login-button').click()

        #login screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'login-button')))
        h.find_element_by_css_selector('#username').send_keys('sans')
        h.find_element_by_css_selector('#password').send_keys('sans')
        h.find_element_by_id('login-button').click()

        #manage crew - assignments screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'manage-crews-button')))
        h.find_element_by_id('manage-crews-button').click()

        #manage crew screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'add-crew-button')))
        crew_div = h.find_element_by_class_name('crew-div')
        self.assertTrue(crew_div.is_displayed())
        h.find_element_by_id('add-crew-button').click()

        #add crew screen test incorrect addition
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'add-crew-button')))
        h.find_element_by_css_selector('#captain_name').send_keys('John')
        h.find_element_by_css_selector('#captain_surname').send_keys('Smith')
        h.find_element_by_id('add-crew-button').click()

        WebDriverWait(h, WAIT_TIME).until(EC.element_to_be_clickable((By.ID, 'error')))
        incorrect_crew_addition = h.find_element_by_id('error')
        self.assertTrue(incorrect_crew_addition.is_displayed())

        h.find_element_by_css_selector('#captain_name').send_keys('1')
        h.find_element_by_id('member-name-0').send_keys('Member1')
        h.find_element_by_id('member-surname-0').send_keys('Surname1')

        h.find_element_by_id('add-member-button').click()
        h.find_element_by_id('member-name-1').send_keys('Member2')
        h.find_element_by_id('member-surname-1').send_keys('Surname2')
        h.find_element_by_id('add-crew-button').click()

        # manage crew screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.CLASS_NAME, 'crew-div')))
        crew_div = h.find_elements_by_class_name('crew-div')
        self.assertEqual(len(crew_div), 2)

        #index of manage crews
        h.get(self.live_server_url + '/static/crewmanager/index.html')
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'manage-assignments-button')))
        h.find_element_by_id('manage-assignments-button').click()

        #crew assignments screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'manage-crew-button-2')))
        h.find_element_by_id('manage-crew-button-2').click()

        #manage assignments incorrect
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'assign-button')))
        h.find_element_by_id('assign-button').click()

        WebDriverWait(h, WAIT_TIME).until(EC.element_to_be_clickable((By.ID, 'error')))
        incorrect_crew_assignment = h.find_element_by_id('error')
        self.assertTrue(incorrect_crew_assignment.is_displayed())

        el = h.find_element_by_id('select')
        el.find_element_by_id('option-2').click()
        h.find_element_by_id('assign-button').click()

        # crew assignments screen
        WebDriverWait(h, WAIT_TIME).until(EC.presence_of_element_located((By.ID, 'manage-crew-button-2')))
        manage_crew_button = h.find_element_by_id('manage-crew-button-2')
        self.assertTrue(manage_crew_button.is_displayed())