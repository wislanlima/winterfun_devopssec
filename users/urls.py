from django.urls import path, include
from django.contrib.auth import views as auth_views

from users.views import (
    UserListView,
    signup,
    SignupView,
    LoginView,
    password_change,
    GetUserAPIView,
)


urlpatterns = [
    path("api/me/", GetUserAPIView.as_view(), name="get-user"),
    path("signup/", SignupView.as_view(), name="signup-user"),
    path("signup2/", signup, name="signup-user2"),

    path("all/", UserListView.as_view(), name="user-list"),
    path("login/", LoginView.as_view(), name="login-user"),
    path("updatepwd/", password_change, name="update-password"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logged_out.html"),
        name="logout-user",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
