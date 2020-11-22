from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    """New class called CustomUser that subclasses AbstractUser and removed the username field"""

    ## Part of AbstractUser
    # first_name 
    # last_name
    # date_joined

    email = models.EmailField(_('email address'), unique=True)
    favourite_language = models.CharField(max_length=30,blank=True)
    bio = models.TextField(max_length=200, blank=True, verbose_name="Biography")
    github_url = models.URLField(blank=True)

    # remove username and use email as the unique identifier
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email