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

from .models import Client, Photo, Trip, Purchase, Payment


def index(request):
    #request.session['destination'] = request.POST['destination']
    #request.session['origin'] = request.POST['origin']
    # latest_question_list = Questao.objects.all()
    return render(request, 'space_trip/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstname = request.POST['firstname']
        surname = request.POST['surname']
        birthday = request.POST['birthday']
        birthday.strftime('%d/%m/%Y')
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
    if request.method == 'POST' and request.FILES.get('myfile') is not None:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        u = request.user
        try:
            photo = Photo.objects.get(user=u)
            photo.photo_url = uploaded_file_url
        except Photo.DoesNotExist:
            photo = Photo(user=u, photo_url=uploaded_file_url)
        photo.save()
        return render(request, 'space_trip/profile.html', {'uploaded_file_url': uploaded_file_url})
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

def tripManagement(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_superuser:
        destination = request.POST['destination']
        origin = request.POST['origin']
        departure_date = request.POST['departure_date']
        return_date = request.POST['return_date']
        price = request.POST['price']
        spaceship = request.POST['spaceship']
        number_of_passengers = request.POST['number_of_passengers']
        trip = Trip(origin=origin, destination=destination, departure_date=departure_date, return_date=return_date, price=price, spaceship=spaceship, number_of_passengers=number_of_passengers)
        trip.save()
        return HttpResponseRedirect(reverse('space_trip:trip-list'))
    else:
        return render(request, 'space_trip/trip-management.html')

def catchDataFromIndex(request):
    if request.POST.get('destination') is not None and request.POST.get('origin') is not None:
        destination = request.POST['destination']
        origin = request.POST['origin']
        return render(request, 'space_trip/plan-trip.html', {'destination':destination,'origin':origin})
    return render(request, 'space_trip/index.html')

def planTrip(request):
    print("AAA")
    trips = Trip.objects.filter(origin=request.POST['origin'], destination=request.POST['destination'], departure_date=request.POST['departure_date'], return_date=request.POST['return_date'])
    if trips.count() > 0:
        print("BBBB")
        request.session['origin'] = request.POST['origin']
        request.session['destination'] = request.POST['destination']
        request.session['departure_date'] = request.POST['departure_date']
        request.session['return_date'] = request.POST['return_date']
        return render(request, 'space_trip/available-trips.html')
    else:
        print("CCCC")
        messages.error(request, 'Não existem viagens com estes atributos.')
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
    trip = Trip.objects.get(destination=request.POST['destination'], origin=request.POST['origin'], departure_date=request.POST['departure_date'], return_date = request.POST['return_date'], price = request.POST['price'], spaceship = request.POST['spaceship'],  number_of_passengers = request.POST['number_of_passengers'])
    total_price = trip.price * trip.number_of_passengers
    user = request.user
    purchase = Purchase(trip, user, total_price)
    purchase.save()

def payment(request):
    return render(request, 'space_trip/payment.html')

def aboutUs(request):
    return render(request, 'space_trip/about-us.html')

def onewaytrip(request):
    return render(request, 'space_trip/onewaytrip.html')

def tripList(request):
    trip_list = Trip.objects.all()
    return render(request, 'space_trip/trip-list.html', {'trip_list': trip_list})

def clientList(request):
    client_list = Client.objects.all()
    return render(request, 'space_trip/client-management.html', {'client_list': client_list})

@permission_required('space_trip.trip-management', login_url=reverse_lazy('space_trip:login'))
def deleteTrip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return HttpResponseRedirect(reverse('space_trip:trip-list'))

@permission_required('space_trip.trip-management', login_url=reverse_lazy('space_trip:login'))
def deleteClient(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    return HttpResponseRedirect(reverse('space_trip:client-management'))

def availableTrips(request):
    print("AAAAAAAAAAAAA")
    if request.session.get('destination') is not None and request.session.get('origin') is not None and request.session.get('departure_date') is not None and request.session.get('return_date') is not None:
        destination = request.session.get('destination')
        origin = request.session.get('origin')
        departure_date = request.session.get('departure_date')
        return_date = request.session.get('return_date')
        trips = Trip.objects.filter(origin=origin, destination=destination, departure_date=departure_date, return_date=return_date)
        return render(request, 'space_trip/trip-list.html', {'trips': trips})
    else:
        messages.error(request, 'Não sei o que escrever aqui,mas faz sentido dar erro')
        return render(request, 'space_trip/plan-trip.html')
    return render(request, 'space_trip/trip-list.html')