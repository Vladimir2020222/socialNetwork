from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView as DefaultLogoutView, LoginView as DefaultLoginView, \
    PasswordChangeView as DefaultPasswordChangeView, PasswordChangeDoneView as DefaultPasswordChangeDoneView
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView


class LogoutView(DefaultLogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('main')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


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


# TODO implement password reset system and ProfileView


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class UserProfileView(TemplateView):
    template_name = 'accounts/user_profile.html'

