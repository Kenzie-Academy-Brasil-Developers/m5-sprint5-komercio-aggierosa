from django.db import models
from django.contrib.auth.models import AbstractUser

from Users.utils import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)	 
    last_name =	models.CharField(max_length=50)	
    is_seller = models.BooleanField()	

    username = None

    REQUIRED_FIELDS= ["first_name", "last_name"]
    USERNAME_FIELD = "email"

    objects = CustomUserManager()
