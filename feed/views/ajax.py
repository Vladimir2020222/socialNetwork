from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from feed.config import ADDITIONAL_POSTS_COUNT
from feed.forms import CommentForm, AnswerForm
from feed.models import Post, Comment
from feed.services import like_or_dislike_object
from feed.services.posts import get_random_posts, get_random_subscriptions_posts


User = get_user_model()


class LikeAjaxView(View):
    action: int = None
    model = None

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        obj = self.get_object()
        user = request.user
        like_or_dislike_object(obj, user, self.action)
        return HttpResponse('')

    def get_object(self):
        if self.model is None:
            raise ImproperlyConfigured('model is not provided, impossible to get object,'
                                       ' define model or override get_object')
        queryset = self.model._default_manager
        pk = self.request.POST.get(f'{self.model._meta.model_name}_pk')
        return get_object_or_404(queryset, pk=pk)


class PostLikeAjaxView(LikeAjaxView):
    model = Post


class CommentLikeAjaxView(LikeAjaxView):
    model = Comment


@require_POST
def send_comment(request):
    form = CommentForm(request=request, data=request.POST)
    if form.is_valid():
        form.save()
    return HttpResponse('')


@require_POST
def send_answer_to_comment(request):
    form = AnswerForm(request=request, data=request.POST)
    if form.is_valid():
        form.save()
    return HttpResponse('')


@require_POST
def get_post_comments(request):
    pk = request.POST.get('post_pk')
    context = {'post': Post.objects.get(pk=pk)}
    return render(request, 'feed/renderable/comments.html', context)


@require_POST
def get_additional_posts(request):
    is_subscriptions = request.POST.get('subscriptions')
    n = request.POST.get('n', ADDITIONAL_POSTS_COUNT)
    if is_subscriptions:
        posts = get_random_subscriptions_posts(request.users, n=n)
    elif author_pk := request.POST.get('author_pk'):
        if is_subscriptions:
            raise ValueError("author_pk and subscriptions = True can't be used together")
        posts = Post.objects.exclude_viewed(request.user).filter(author_pk=author_pk)[:n]
    else:
        posts = get_random_posts(user=request.user, n=n)
    context = {'posts': posts}
    return render(request, 'feed/renderable/posts.html', context)


@require_POST
def subscribe(request):
    user = User.objects.get(pk=request.POST.get('user_pk'))
    if user == request.user:
        raise ValueError('impossible to subscribe yourself')
    user.subscribers.add(request.user)
    return HttpResponse('')


def unsubscribe(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.POST.get('user_pk'))
        user.subscribers.remove(request.user)
    return HttpResponse('')


def add_post_to_viewed(request):
    if request.user.is_authenticated and False:
        post = Post.objects.get(pk=request.POST.get('post_pk'))
        request.user.viewed_posts.add(post)
    return HttpResponse('')
