from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from . import validator

from django import forms
from django.contrib.auth import get_user_model

from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# TODO: VERRIFICAR SE ESSE FORM FUNCIONA
class SignupForm1(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(),
        max_length=30,
        required=True,
    )
    email = forms.CharField(
        widget=forms.EmailInput(),
        max_length=100,
        required=True,
    )
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Confirm your password."
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")


class LoginForm(forms.Form):
    """user login form"""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "username"]
        error_class = "error"

    def clean(self):
        super(CustomUserCreationForm, self).clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            self._errors["password"] = self.error_class(
                ["Passwords do not match. Try again"]
            )
        return self.cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email"]
        error_class = "error"


# TODO: FORM REVER ISSO CHANGE PASSWORD FORM
class change_password_form(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(), label="Old password", required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(), label="New password", required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm new password", required=True
    )

    class Meta:
        model = User
        fields = ("old_password", "new_password", "confirm_password")

    def clean(self):
        super(change_password_form, self).clean()
        pkid = self.cleaned_data.get("pkid")
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        user = User.objects.get(pk=pkid)
        if not user.check_password(old_password):
            self._errors["old_password"] = self.error_class(
                ["Old password do not match."]
            )
        if new_password != confirm_password:
            self._errors["new_password"] = self.error_class(["Passwords do not match."])
        return self.cleaned_data
