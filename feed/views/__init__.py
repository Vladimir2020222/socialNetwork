from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from feed.forms import CreatePostFrom, UpdatePostFrom
from feed.models import Post
from feed.mixins import VerifyAuthorMixin
from feed.services.posts import get_random_subscriptions_posts, get_random_posts
from feed.config import INITIAL_POSTS_COUNT


def main(request):
    context = {
        'posts': get_random_posts(user=request.user, n=INITIAL_POSTS_COUNT),
        'is_subscriptions': False
    }
    return render(request, 'feed/main.html', context)


def subscriptions(request):
    context = {
        'posts': get_random_subscriptions_posts(request.user, n=INITIAL_POSTS_COUNT),
        'is_subscriptions': False
    }
    return render(request, 'feed/main.html', context)


@method_decorator(login_required, 'dispatch')
class CreatePostView(CreateView):
    model = Post
    form_class = CreatePostFrom
    success_url = reverse_lazy('main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class UpdatePostView(UpdateView, VerifyAuthorMixin):
    model = Post
    form_class = UpdatePostFrom
    success_url = reverse_lazy('main')
    template_name_suffix = '_update'

    def delete(self, request, *args, **kwargs):
        return redirect('post_delete', kwargs={'pk': self.kwargs.get('pk')})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class DeletePostView(DeleteView, VerifyAuthorMixin):
    model = Post
    success_url = reverse_lazy('main')


class PostDetailView(DetailView):
    model = Post
