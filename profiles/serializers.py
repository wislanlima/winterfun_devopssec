from django_countries.serializer_fields import CountryField
from rest_framework import fields, serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "id",
            "first_name",
            "last_name",
            "slug",
            "avatar",
            "about_me",
            "gender",
            "country",
            "city",
            "created_at",
            "updated_at",
        ]

    def get_full_name(self, obj):
        first_name = obj.profile.first_name.title()
        last_name = obj.profile.last_name.title()
        return f"{first_name} {last_name}"


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "slug",
            "phone_number",
            "avatar",
            "about_me",
            "gender",
            "country",
            "city",
            "created_at",
            "updated_at",
        ]
