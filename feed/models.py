from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet, Manager
from django.urls import reverse
from socialNetwork.utils import RequestRenderableMixin

User = get_user_model()


class Image(models.Model):
    """Post image"""

    img = models.ImageField(upload_to='posts/%Y/%m/%d/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images', related_query_name='image')


class LikeablePermission(models.Model):
    """Permission for models that can be liked by user"""

    likes = models.ManyToManyField(User,
                                   related_name='%(app_label)s_liked_%(class)ss',
                                   related_query_name='%(app_label)s_liked_%(class)s')
    dislikes = models.ManyToManyField(User,
                                      related_name='%(app_label)s_disliked_%(class)ss',
                                      related_query_name='%(app_label)s_disliked_%(class)s')

    class Meta:
        abstract = True


class DatePermission(models.Model):
    """Permission for models whose time publish and time update should be saved"""

    date_published = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(LikeablePermission, DatePermission, RequestRenderableMixin):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='posts', related_query_name='post')
    title = models.CharField(max_length=80)
    text = models.TextField(max_length=15000)

    template_name = 'feed/renderable/post.html'

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})

    @property
    def comment_form(self):
        from feed.forms import CommentForm
        return CommentForm(post=self)

    def get_context(self):
        return {
            'post': self,
        }


class CommentQuerySet(QuerySet):
    def first_level(self):
        return self.filter(answer_to__isnull=True)


class Comment(LikeablePermission, DatePermission, RequestRenderableMixin):
    objects = Manager.from_queryset(CommentQuerySet)()

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='comments', related_query_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                             related_query_name='comment')
    answer_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='answers',
                                  related_query_name='answer', blank=True, null=True)

    text = models.TextField(max_length=5000)

    template_name = 'feed/renderable/comment.html'
    max_level = 5

    def __str__(self):
        return self.text

    def get_context(self):
        return {
            'comment': self,
            'answers': self.answers.all()
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

    @property
    def answer_form(self):
        from .forms import AnswerForm
        return AnswerForm(post=self.post, answer_to=self)

    def clean(self):
        if self.level > self.max_level:
            raise ValidationError('Something went wrong')
        if self.answer_to == self:
            raise ValidationError('Something went wrong')
