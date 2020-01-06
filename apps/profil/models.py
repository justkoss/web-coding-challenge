from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    CustomUser = UserManager

    def __str__(self):
        return self.email
