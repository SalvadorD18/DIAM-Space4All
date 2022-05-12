from django.urls import include, path
from . import views
from django.utils import timezone
import datetime
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# (. significa que importa views da mesma directoria)

app_name = 'space_trip'

urlpatterns = [path("", views.index, name="index"),
               path("register", views.register, name="register"),
               path("logoutview", views.logoutview, name="logoutview"),
               path("login", views.user_login, name="user_login"),
               path("profile", views.profile, name="profile"),
               path("uploadPhoto", views.uploadPhoto, name="uploadPhoto"),
               path("destinations", views.destinations, name="destinations"),
               path("moon", views.moon, name="moon"),
               path("mercury", views.mercury, name="mercury"),
               path("venus", views.venus, name="venus"),
               path("earth", views.earth, name="earth"),
               path("mars", views.mars, name="mars"),
               path("jupiter", views.jupiter, name="jupiter"),
               path("saturn", views.saturn, name="saturn"),
               path("uranus", views.uranus, name="uranus"),
               path("neptune", views.neptune, name="neptune"),
               path("payment", views.payment, name="payment"),
               path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('spicy space/favicon.ico'))),
               path("gallery", views.gallery, name="gallery"),
               path("promotions", views.promotions, name="promotions"),
               path("about-us", views.aboutUs, name="about-us"),
               path("onewaytrip", views.onewaytrip, name="onewaytrip"),
               path("plan-trip", views.planTrip, name="planTrip"),
               path("edit-profile", views.editProfile, name="edit-profile"),
               path("editUserData", views.editUserData, name="editUserData"),
               path("client-management", views.clientList, name="client-management"),
               path("trip-management", views.tripManagement, name="trip-management"),
               path("catchDataFromIndex", views.catchDataFromIndex, name="catchDataFromIndex"),
               path("trip-list", views.tripList, name="trip-list"),
               path("<int:trip_id>/deleteTrip", views.deleteTrip, name="deleteTrip"),
               path("available-trips", views.availableTrips, name="available-trips"),
               path("<int:client_id>/deleteClient", views.deleteClient, name="deleteClient")
               ]
