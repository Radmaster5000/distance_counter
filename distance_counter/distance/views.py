from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def index(request):
    return render(request, "distance/index.html")

def log(request):
    return render(request, "distance/log.html")

def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('log')

        form = LoginForm()
        return render(request, 'distance/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Hello {username.title()}, let's get logging!")
                return redirect('log')
            
        # form isn't valid or unauthenticated user
        messages.error(request, f"Invalid username or password, please try again!")
        return render(request, 'distance/login.html', {'form': form})
    
def sign_out(request):
    logout(request)
    messages.success(request, f"You're now logged out. Why are you logging out?")
    return redirect('login')