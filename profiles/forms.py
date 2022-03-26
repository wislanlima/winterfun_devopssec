from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "about_me",
            "gender",
            "country",
            "city",
        )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "about_me",
            "gender",
            "country",
            "city",
        )
