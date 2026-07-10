from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class Role(models.TextChoices):
    Manager = 'manager', 'Manager'
    Dispatcher = 'dispatcher', 'Dispatcher'
    Driver = 'driver', 'Driver'



class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=Role.choices)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email