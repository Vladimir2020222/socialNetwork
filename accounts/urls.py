from django.urls import path
from .views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView, ProfileView, RegisterView, \
    UserDetailView, UpdateProfileView, change_ava

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('password_change', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('user/<str:username>', UserDetailView.as_view(), name='user'),
    path('profile_change', UpdateProfileView.as_view(), name='profile_change'),
    path('change_ava', change_ava, name='change_ava')
]
