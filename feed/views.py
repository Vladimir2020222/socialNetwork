from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views import View
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from .forms import CreatePostFrom, UpdatePostFrom, CommentForm, AnswerForm
from feed.models import Post, Comment
from .mixins import VerifyAuthorMixin
from .services import like_or_dislike_object


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


class LikeAjaxView(View):
    action: int = None
    model: Model = None

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

