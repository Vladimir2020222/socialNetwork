from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from feed.forms import CreatePostFrom, UpdatePostFrom
from feed.models import Post


class MainView(TemplateView):
    template_name = 'feed/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context


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
class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostFrom
    success_url = reverse_lazy('main')
    template_name_suffix = '_update'

    def _verify_author(self):
        if self.request.user != Post.objects.get(pk=self.kwargs.get('pk')).author:
            return PermissionDenied()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self._verify_author()
        super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
