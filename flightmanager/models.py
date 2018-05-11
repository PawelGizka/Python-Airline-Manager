from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q

from django.core.exceptions import ValidationError

# Create your models here.
class Airplane(models.Model):
    registration_number = models.CharField(max_length=10)
    #max number of seats for airbus a380-800
    seat_number = models.IntegerField(validators=[MaxValueValidator(615), MinValueValidator(1)])

    def __str__(self):
        return "Airplane({}, {})".format(self.registration_number, str(self.seat_number))


class Flight(models.Model):
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    departure_airport = models.CharField(max_length=20)
    arrival_airport = models.CharField(max_length=20)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)

    def clean(self):
        collision_departure = Flight.objects\
            .filter(airplane_id__exact=self.airplane_id)\
            .filter(departure_date__lte=self.departure_date)\
            .filter(arrival_date__gte=self.departure_date)

        collision_arrival = Flight.objects \
            .filter(airplane_id__exact=self.airplane_id) \
            .filter(departure_date__lte=self.arrival_date) \
            .filter(arrival_date__gte=self.arrival_date)

        if collision_departure or collision_arrival:
            raise ValidationError('There is other flight at the same time using the same aircraft')

        if self.arrival_airport == self.departure_airport:
            raise ValidationError('Flight can not have same departure and arrival airport')

        if self.arrival_date < self.departure_date:
            raise ValidationError('Flight can not have earlier arrival than departure date')

    def __str__(self):
        return "Flight({}, {}, {}, {}, {})"\
            .format(self.departure_date.strftime("%Y-%m-%d %H:%M"),
                    self.arrival_date.strftime("%Y-%m-%d %H:%M"),
                    self.departure_airport,
                    self.arrival_airport,
                    str(self.airplane_id))


class Passanger(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return "Passenger({}, {})".format(self.name, self.surname)

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passanger, on_delete=models.CASCADE)
    #max 30kg of luggage per passenger
    luggage_weight = models.IntegerField(validators=[MaxValueValidator(30), MinValueValidator(0)])

    def __str__(self):
        return "Ticket({}, {}, {})".format(str(self.flight_id), str(self.passenger_id), str(self.luggage_weight))
