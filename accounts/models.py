from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from django.urls import reverse
from django.utils import timezone


class UserManager(DefaultUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()
    ava = models.ImageField(upload_to='users/avatars/%Y/%m/%d/', default='users/default_ava.jpg')
    age = models.PositiveSmallIntegerField()
    date_birth = models.DateField()
    subscriptions = models.ManyToManyField('accounts.User',
                                           related_name='subscribers',
                                           related_query_name='subscriber')

    class Meta:
        db_table = 'auth_user'

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.username})

    def save(self, *args, **kwargs):
        now = timezone.now().date()
        age = now.year - self.date_birth.year - 1
        if now.month >= self.date_birth.month and now.day >= self.date_birth.day:
            age += 1
        self.age = age
        print(age)
        super().save(*args, **kwargs)
