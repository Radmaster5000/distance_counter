from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Distance, Office, Person, Unit

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
       

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = '__all__'

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'