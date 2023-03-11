from random import randint

from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone


class UserManager(DefaultUserManager):
    def create(self, **kwargs):
        if 'username' not in kwargs:
            kwargs['username'] = self.get_random_username()
        return super().create(**kwargs)

    @classmethod
    def get_random_username(cls):
        while True:
            n = randint(0, 1000000000)
            username = 'кокаиновай_нухач_%s' % n
            if not User.objects.filter(username=username).exists():
                return username


class User(AbstractUser):
    REQUIRED_FIELDS = ['date_birth']
    objects = UserManager()
    ava = models.ImageField(upload_to='users/avatars/%Y/%m/%d/', default='users/default_ava.jpg')
    date_birth = models.DateField()
    subscriptions = models.ManyToManyField('accounts.User',
                                           related_name='subscribers',
                                           related_query_name='subscriber')

    viewed_posts = models.ManyToManyField('feed.Post',
                                          related_name='viewers',
                                          related_query_name='viewer')

    class Meta:
        db_table = 'auth_user'

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.username})

    def save(self, *args, **kwargs):
        if self.username == '':
            self.username = self.__class__.objects.get_random_username()
        super().save(*args, **kwargs)

    @property
    def age(self):
        if hasattr(self, '__age'):
            return self.__age
        now = timezone.now().date()
        age = now.year - self.date_birth.year - 1
        if now.month >= self.date_birth.month and now.day >= self.date_birth.day:
            age += 1
        self.__age = age
        return self.__age

    def total_likes(self):
        return self.posts.aggregate(likes=Count('likes'))['likes']

    def total_dislikes(self):
        return self.posts.aggregate(dislikes=Count('dislikes'))['dislikes']
