from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from . import validator as validator


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_("Users must submit a username"))

        if email:
            email = self.normalize_email(email)
            validator.email_validator(email)
        else:
            raise ValueError(_("Base User Account: An email address is required"))

        user = self.model(username=username, email=email, **extra_fields)

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))

        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            email = self.normalize_email(email)
            validator.email_validator(email)
        else:
            raise ValueError(_("Admin Account: An email address is required"))

        user = self.create_user(username, email, password, **extra_fields)
        user.save(using=self._db)
        return user
