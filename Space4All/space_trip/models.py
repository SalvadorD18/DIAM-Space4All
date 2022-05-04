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

class Aluno(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 course = models.CharField(max_length=50)

class Foto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_url = models.URLField(max_length=100)