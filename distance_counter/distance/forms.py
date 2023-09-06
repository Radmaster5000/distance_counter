from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Distance

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)

class LogForm(forms.ModelForm):
    class Meta:
        model = Distance
        fields = ['date', 'person', 'distance', 'unit']