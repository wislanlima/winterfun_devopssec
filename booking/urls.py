from django.urls import path, include
from django.contrib.auth import views as auth_views

from booking.views import index

app_name = "booking"

urlpatterns = [
    path("", index, name="index"),
]
