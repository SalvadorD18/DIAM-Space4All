from time import strftime

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class Client(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 firstname = models.CharField(max_length=50)
 surname = models.CharField(max_length=50)
 birthday = models.DateTimeField('birthday')
 gender = models.CharField(max_length=50)
 planetionality = models.CharField(max_length=50)

class Photo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_url = models.URLField(max_length=100)

class Trip(models.Model):
 origin = models.CharField(max_length=50)
 destination = models.CharField(max_length=50)
 departure_date = models.DateTimeField('departure_date')
 return_date = models.DateTimeField('return_date')
 price = models.IntegerField(default=600)
 spaceship = models.CharField(max_length=50)
 number_of_passengers = models.IntegerField(default=1)
 #available_seats = models.IntegerField(default=60)


class Purchase(models.Model):
 trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 total_price = models.IntegerField(default=0)
 is_payed = models.BooleanField(default=False)

class Payment(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
 cardName = models.CharField(max_length=50)
 cardNumber = models.CharField(max_length=16)
 expirationDate = models.DateTimeField('Expiration Date')
 cvv = models.CharField(max_length=3)

class Planets(models.Model):
 name = models.CharField(max_length=50)
 name_pt = models.CharField(max_length=50)
 details = models.CharField(max_length=3000000000)
