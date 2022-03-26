from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from django.core.cache import cache

from users.forms import UserCreationForm, SignupForm1

from users.forms import SignupForm
from django.views.generic.edit import FormView

from winterfun import redis_key_schema
from winterfun.redis_key_schema import key_schema
from . import forms
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, viewsets, parsers
from .renderers import UserJSONRenderer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.response import Response

User = get_user_model()
ONE_HOUR = 60 * 60

"""API REQUEST START HERE"""


class GetUserAPIView(APIView):
    """
    This is an api call for the current user logged
    It use the serializer class rest_framework
    Link: api/me/
    Done!
    """
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserJSONRenderer]

    def get(self, request):
        username = self.request.user
        user_profile = User.objects.get(username=username)
        serializer = UserSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

"""API end here"""


def signup(request):
    """
    This function allow to register a new user with email and password
    it creates a session on redis for the current registered user
    Using method
    Done
    """
    if request.method == "POST":
        form = SignupForm1(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            # user = authenticate(email=email, password=raw_password)
            print(user)
            login(request, user)
            return redirect("profiles:my-profile")
    else:
        form = SignupForm1()
    return render(
        request, "users/signup.html", {"form": form, "login_url": "/accounts/login"}
    )


class SignupView(FormView):
    """
    This function allow to register a new user with email and password
    it creates a session on redis for the current registered user
    Using the form that was created on users/forms.py
    Done
    """
    form_class = forms.SignupForm
    template_name = "users/signup.html"
    success_url = "profiles:my-profile"

    def form_valid(self, form):
        """process user signup"""
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        if user is not None:
            return redirect(self.success_url)
        return super().form_valid(form)


class LoginView(FormView):
    """
    This function allow the users to log into the application with email and password
    it creates a session on redis for the current user
    Done
    """
    form_class = forms.LoginForm
    success_url = "profiles:my-profile"
    template_name = "users/login.html"

    def form_valid(self, form):
        """process user login"""
        credentials = form.cleaned_data
        user = authenticate(
            username=credentials["email"], password=credentials["password"]
        )

        if user is not None:
            login(self.request, user)
            #print(self.success_url)
            return redirect(self.success_url)
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                "Wrong credentials\
                                please try again",
            )
            return redirect("login-user")


class UserListView(ListView):
    """
    This function shows all users from the database
    If the the function was loaded previously, it loads it from redis cache
    key: winterfun:user:all
    Done
    """
    model = User
    template_name = "users/user_list.html"  # <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        User = get_user_model()
        # Definning the standart key
        key = key_schema().user_list_key()
        cached_result = cache.get(key)

        if not cached_result:
            users = User.objects.all()
            cache.set(key, users, timeout=ONE_HOUR)
            context["users"] = users
            print("NOT FROM CACHE")
            return context
        print("from cache")
        context["users"] = cached_result
        return context

# TODO: PASSWORD_CHANGE needs to be fixed after adding the api calls
@login_required
def password_change(request):
    user = request.user
    print(user.__dict__)
    if request.method == "POST":
        form = forms.change_password_form(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("password_reset_done")
        else:
            messages.error(request, "Please correct the error below.")
    else:

        form = forms.change_password_form(instance=user)

    context = {
        "form": form,
    }

    return render(request, "users/change_password.html", context)