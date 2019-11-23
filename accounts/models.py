from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site

# Create your models here.
class User(AbstractUser):
    follow_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_user')
    # sites = models.ManyToManyField(Site)