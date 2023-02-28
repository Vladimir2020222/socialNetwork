from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet, Manager
from django.forms.renderers import get_default_renderer
from django.forms.utils import RenderableMixin
from django.urls import reverse

User: User = get_user_model()


class Image(models.Model):
    img = models.ImageField(upload_to='posts/%Y/%m/%d/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images', related_query_name='image')


class LikeablePermission(models.Model):

    likes = models.ManyToManyField(User,
                                   related_name='%(app_label)s_liked_%(class)ss',
                                   related_query_name='%(app_label)s_liked_%(class)s')
    dislikes = models.ManyToManyField(User,
                                      related_name='%(app_label)s_disliked_%(class)ss',
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

    @property
    def comment_form(self):
        from feed.forms import CommentForm
        return CommentForm(post=self)


class CommentQuerySet(QuerySet):
    def first_level(self):
        return self.filter(answer_to__isnull=True)


class Comment(LikeablePermission, RenderableMixin):
    objects = Manager.from_queryset(CommentQuerySet)()

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='comments', related_query_name='comment')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                             related_query_name='comment')

    answer_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='answers',
                                  related_query_name='answer', blank=True, null=True)

    text = models.TextField(max_length=5000)

    renderer = get_default_renderer()
    template_name = 'feed/renderable/comment.html'

    def __str__(self):
        return self.text

    def get_context(self):
        return {
            'comment': self
        }

    @property
    def level(self):
        if hasattr(self, '_level'):
            return self._level
        level = 0
        comment = self
        while True:
            if comment.answer_to is not None:
                comment = comment.answer_to
                level += 1
            else:
                self._level = level
                return level

    def clean(self):
        if self.level >= 10:
            raise ValidationError('Comment level is too high')
