from django.contrib.auth.models import AbstractUser

from lib.helpers.behaviors import BaseModelable


class User(BaseModelable, AbstractUser):
    """Model definition for USER."""
    pass
