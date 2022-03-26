from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


def email_validator(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValueError(_("You must provide a valid email address"))
