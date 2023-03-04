from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from django.urls import reverse


class UserManager(DefaultUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()
    ava = models.ImageField(upload_to='users/avatars/%Y/%m/%d/', default='users/default_ava.jpg')

    class Meta:
        db_table = 'auth_user'

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})
