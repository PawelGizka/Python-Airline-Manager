from django.db import models

# Create your models here.
class Airplane(models.Model):
    registration_number = models.CharField(max_length=10)
    seat_number = models.IntegerField()

class Flight(models.Model):
    start_date = models.DateTimeField()
    land_date = models.DateTimeField()
    start_airport = models.CharField(max_length=20)
    land_airport = models.CharField(max_length=20)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)

class Passanger(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)


class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passanger = models.ForeignKey(Passanger, on_delete=models.CASCADE)
    luggage_weight = models.IntegerField()
