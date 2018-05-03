from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'headshot', 'signature']


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'headshot', 'signature']