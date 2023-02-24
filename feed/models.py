from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

User: User = get_user_model()


class Image(models.Model):
    img = models.ImageField(upload_to='posts/%Y/%m/%d/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images', related_query_name='image')


class LikeablePermission(models.Model):

    likes = models.ManyToManyField(User,
                                   related_name='%(app_label)s_liked_%(class)s',
                                   related_query_name='%(app_label)s_liked_%(class)s')
    dislikes = models.ManyToManyField(User,
                                      related_name='%(app_label)s_disliked_%(class)s',
                                      related_query_name='%(app_label)s_disliked_%(class)s')

    class Meta:
        abstract = True


class Post(LikeablePermission):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='posts', related_query_name='post')
    title = models.CharField(max_length=80)
    text = models.TextField(max_length=15000)
    date_published = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})

    __html__ = (lambda self: str(self.title) + str(self.author))


class Comment(LikeablePermission):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='comments', related_query_name='comment')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                             related_query_name='comment')

    answer_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='answers',
                                  related_query_name='answer', blank=True, null=True)

    text = models.TextField(max_length=5000)
