from django.urls import path, include
from django.contrib.auth import views as auth_views

from frontend.views import index

app_name = "frontend"

urlpatterns = [
    path("", index, name="index"),
]
