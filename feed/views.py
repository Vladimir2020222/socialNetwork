from enum import Enum

from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views import View
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.base import TemplateView

from .forms import CreatePostFrom, UpdatePostFrom, CommentForm
from feed.models import Post
from .mixins import MultiFromMixin, VerifyAuthorMixin


class MainView(ListView):
    template_name = 'feed/main.html'
    context_object_name = 'posts'
    model = Post


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


@method_decorator([login_required, atomic], 'dispatch')
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


class PostLikeActions(Enum):
    like = 0
    unlike = 1
    dislike = 2
    undislike = 3


@method_decorator([login_required, ], 'dispatch')
class PostLikeAjaxView(View):
    action = None

    def get(self, request):
        post = get_object_or_404(Post, pk=request.GET.get('post_pk'))
        user = request.user
        match self.action:
            case PostLikeActions.like:
                post.dislikes.remove(user)
                post.likes.add(user)

            case PostLikeActions.unlike:
                post.likes.remove(user)

            case PostLikeActions.dislike:
                post.likes.remove(user)
                post.dislikes.add(user)

            case PostLikeActions.undislike:
                post.dislikes.remove(user)
        return HttpResponse('')


@require_POST
def send_comment(request):
    form = CommentForm(request=request, data=request.POST)
    if form.is_valid():
        form.save()
    return HttpResponse('')

