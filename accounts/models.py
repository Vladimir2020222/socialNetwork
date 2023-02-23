from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models


class UserManager(DefaultUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
