from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class Questao(models.Model):
 questao_texto = models.CharField(max_length=200)
 pub_data = models.DateTimeField('data de publicacao')

 def __str__(self):
  return self.questao_texto


 def foi_publicada_recentemente(self):
  return self.pub_data >= timezone.now() - datetime.timedelta(days=1)

class Opcao(models.Model):
 questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
 opcao_texto = models.CharField(max_length=200)
 votos = models.IntegerField(default=0)

 def __str__(self):
  return self.opcao_texto

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

class TwoWayTrip(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 destination = models.CharField(max_length=50)
 origin = models.CharField(max_length=50)
 departure_date = models.DateTimeField('Departure Date')
 return_date = models.DateTimeField('Return Date')
 number_of_passengers = models.IntegerField(default=1)

class OneWayTrip(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 destination = models.CharField(max_length=50)
 origin = models.CharField(max_length=50)
 departure_date = models.DateTimeField('Departure Date')
 number_of_passengers = models.IntegerField(default=1)


class Trip(models.Model):
 destination = models.CharField(max_length=50)
 origin = models.CharField(max_length=50)
 departure_date = models.DateTimeField('Departure Date')
 return_date = models.DateTimeField('Return Date')
 price = models.IntegerField(default=600)
 spaceship = models.CharField(max_length=50)
 number_of_passengers = models.IntegerField(default=1)

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