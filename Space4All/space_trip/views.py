from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .models import Questao, Opcao, Client, Photo, TwoWayTrip, OneWayTrip, Trip, Purchase, Payment


def index(request):
    #request.session['destination'] = request.POST['destination']
    #request.session['origin'] = request.POST['origin']
    # latest_question_list = Questao.objects.all()
    return render(request, 'space_trip/index.html')

def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'space_trip/detalhe.html', {'questao': questao})

@login_required(login_url='/space_trip/login')
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
    # Apresenta de novo o form para votar
        return render(request, 'space_trip/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção",})
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
 # Retorne sempre HttpResponseRedirect depois de
 # tratar os dados POST de um form
 # pois isso impede os dados de serem tratados
 # repetidamente se o utilizador
 # voltar para a página web anterior.
        return HttpResponseRedirect(reverse('space_trip:resultados', args=(questao.id,)))

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'space_trip/resultados.html', {'questao': questao})

@permission_required('space_trip.add_questao', login_url=reverse_lazy('space_trip:login'))
def view_questao_otimizada(request):
    if request.method == 'POST':
        questao_texto = request.POST['questao']
        pub_data = timezone.now()
        q = Questao(questao_texto=questao_texto, pub_data=pub_data)
        q.save()
        return HttpResponseRedirect(reverse('space_trip:index'))
    else:
        return render(request, 'space_trip/criarquestao.html')

@permission_required('space_trip.add_opcao', login_url=reverse_lazy('space_trip:login'))
def view_opcao_otimizada(request, questao_id):
    if request.method == 'POST':
        questao = Questao.objects.get(pk=questao_id)
        questao.opcao_set.create(opcao_texto=request.POST['opcao'], votos=0)
        return HttpResponseRedirect(reverse('space_trip:detalhe', args=(questao.id,)))
    else:
        questao = get_object_or_404(Questao, pk=questao_id)
        return render(request, 'space_trip/novaopcao.html', {'questao': questao})

@permission_required('space_trip.add_opcao', login_url=reverse_lazy('space_trip:login'))
def apagarquestao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('space_trip:index'))

@permission_required('space_trip.add_opcao', login_url=reverse_lazy('space_trip:login'))
def apagaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'space_trip/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção",})
    else:
        opcao_seleccionada.delete()
        return HttpResponseRedirect(reverse('space_trip:detalhe', args=(questao.id,)))

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstname = request.POST['firstname']
        surname = request.POST['surname']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        planetionality = request.POST['planetionality']
        u = User.objects.create_user(username, password=password, email=email)
        c = Client(user=u, firstname=firstname, surname=surname, birthday=birthday, gender=gender, planetionality=planetionality)
        c.save()
        user = authenticate(username=username, password=password)
        return render(request, 'space_trip/login.html')
    else:
        return render(request, 'space_trip/register.html')


def user_login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('space_trip:index'))

        else:
            return render(request, 'space_trip/register.html')
    except MultiValueDictKeyError:
        return render(request, 'space_trip/login.html')


def profile(request):
    try:
        uploaded_file_url = request.user.photo.photo_url
        return render(request, 'space_trip/profile.html', {'uploaded_file_url': uploaded_file_url})
    except ObjectDoesNotExist:
        return render(request, 'space_trip/profile.html')

def editProfile(request):
    try:
        uploaded_file_url = request.user.photo.photo_url
        return render(request, 'space_trip/edit-profile.html', {'uploaded_file_url': uploaded_file_url})
    except ObjectDoesNotExist:
        return render(request, 'space_trip/edit-profile.html')

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('space_trip:index'))

@login_required(login_url='space_trip/register.html')
def uploadPhoto(request):
    print("aaaaaa")
    if request.method == 'POST' and request.FILES.get('myfile') is not None:
        print("bbbbb")
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        u = request.user
        try:
            photo = Photo.objects.get(user=u)
            photo.photo_url = uploaded_file_url
            print("ccccc")
        except Photo.DoesNotExist:
            print("ddddd")
            photo = Photo(user=u, photo_url=uploaded_file_url)
        photo.save()
        return render(request,'space_trip/profile.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'space_trip/profile.html')

def destinations(request):
    return render(request, 'space_trip/destinations.html')

def moon(request):
    return render(request, 'space_trip/moon.html')

def mercury(request):
    return render(request, 'space_trip/mercury.html')

def venus(request):
    return render(request, 'space_trip/venus.html')

def earth(request):
    return render(request, 'space_trip/earth.html')

def mars(request):
    return render(request, 'space_trip/mars.html')

def jupiter(request):
    return render(request, 'space_trip/jupiter.html')

def saturn(request):
    return render(request, 'space_trip/saturn.html')

def uranus(request):
    return render(request, 'space_trip/uranus.html')

def neptune(request):
    return render(request, 'space_trip/neptune.html')

def gallery(request):
    return render(request, 'space_trip/gallery.html')

def promotions(request):
    return render(request, 'space_trip/promotions.html')

def admincreatetrip(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            destination = request.POST['destination']
            origin = request.POST['origin']
            departure_date = request.POST['departure_date']
            return_date = request.POST['return_date']
            price = request.POST['price']
            spaceship = request.POST['spaceship']
            number_of_passengers = request.POST['number_of_passengers']
            trip = Trip(destination=destination, origin=origin, departure_date=departure_date, return_date=return_date, price=price, spaceship=spaceship)
            trip.save()
    except MultiValueDictKeyError:
        return render(request, 'space_trip/admincreatetrip.html')

def planTrip(request):
    print("dddddd")
    if request.method == 'POST':
        # if request.session['destination'] is not None:
        #     desti = request.session.get('destination')
        #     ori = request.session['origin']
        #     request.session.flush()
        # else:
        desti = request.POST['destination']
        ori = request.POST['origin']
        try:
            trip = Trip.objects.get(destination=desti, origin=ori, departure_date=request.POST['departure_date'], return_date=request.POST['return_date'])
            print("cccccccc")
            print("bbbbbbbbb")
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            purchase = Purchase(trip, user)
            purchase.save()
            return render(request, 'space_trip/payment.html')
        except Trip.DoesNotExist:
            print("aaaaa")
            messages.error(request, "Não há viagens disponíveis com estes dados.")
            return render(request, 'space_trip/plan-trip.html')
    else:
        return render(request, 'space_trip/plan-trip.html')

def editUserData(request):
    user = request.user
    user.email = request.POST['email']
    user.save()
    user.client.save()
    return render(request, 'space_trip/profile.html')

def payment(request):
    return render(request, 'space_trip/payment.html')



def purchase(request):
    trip = Trip.objects.get(destination = request.POST['destination'], origin = request.POST['origin'], departure_date = request.POST['departure_date'], return_date = request.POST['return_date'], price = request.POST['price'], spaceship = request.POST['spaceship'],  number_of_passengers = request.POST['number_of_passengers'])
    total_price = trip.price * trip.number_of_passengers
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    purchase = Purchase(trip, user, total_price)
    purchase.save()

def payment(request):
    return render(request, 'space_trip/payment.html')

def aboutUs(request):
    return render(request, 'space_trip/about-us.html')

def onewaytrip(request):
    return render(request, 'space_trip/onewaytrip.html')

def clientManagement(request):
    return render(request, 'space_trip/client-management.html')

def tripManagement(request):
    return render(request, 'space_trip/trip-management.html')