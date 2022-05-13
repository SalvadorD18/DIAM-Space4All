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
               path("<str:name>", views.planet, name="planet"),
               path("payment", views.payment, name="payment"),
               path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('spicy space/favicon.ico'))),
               path("about-us", views.aboutUs, name="about-us"),
               path("plan-trip", views.planTrip, name="planTrip"),
               path("edit-profile", views.editProfile, name="edit-profile"),
               path("editUserData", views.editUserData, name="editUserData"),
               path("client-management", views.userList, name="client-management"),
               path("trip-management", views.tripManagement, name="trip-management"),
               path("catchDataFromIndex", views.catchDataFromIndex, name="catchDataFromIndex"),
               path("trip-list", views.tripList, name="trip-list"),
               path("<int:trip_id>/deleteTrip", views.deleteTrip, name="deleteTrip"),
               path("available-trips", views.availableTrips, name="availableTrips"),
               path("<int:user_id>/deleteUser", views.deleteUser, name="deleteUser"),
               path("purchase", views.purchase, name="purchase"),
               path("trip-purchase-successful", views.tripPurchaseSuccessful, name="tripPurchaseSuccessful")
               ]
