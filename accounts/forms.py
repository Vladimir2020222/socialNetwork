from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.utils import timezone

User = get_user_model()


class UserCreationForm(DefaultUserCreationForm):
    class Meta(DefaultUserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_birth')
        widgets = {'date_birth': forms.SelectDateWidget(years=range(1900, timezone.now().year))}

