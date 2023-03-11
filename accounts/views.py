from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LogoutView as DefaultLogoutView, LoginView as DefaultLoginView, \
    PasswordChangeView as DefaultPasswordChangeView, PasswordChangeDoneView as DefaultPasswordChangeDoneView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from feed.config import INITIAL_POSTS_COUNT
from .forms import UserCreationForm, UpdateUserForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.edit import UpdateView

User = get_user_model()


class LogoutView(DefaultLogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('main')


class LoginView(DefaultLoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.save()
        login(self.request, form.instance)
        return super().form_valid(form)


class PasswordChangeView(DefaultPasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDoneView(DefaultPasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


# TODO password reset system


class UpdateProfileView(UpdateView):
    template_name = 'accounts/profile_change.html'
    form_class = UpdateUserForm

    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    posts_in_profile = INITIAL_POSTS_COUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.request.user
        context['posts'] = self.request.user.posts.order_by('-date_published')[:self.posts_in_profile]
        return context


class UserDetailView(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'owner'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    posts_in_profile = INITIAL_POSTS_COUNT

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object == self.request.user:
            return redirect('profile')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.order_by('-date_published')[:self.posts_in_profile]
        return context


@require_POST
def change_ava(request):
    file = request.FILES.get('ava')
    user = request.user
    user.ava = file
    user.save()
    return redirect(user)
