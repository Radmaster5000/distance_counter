from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, LogForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Distance

# Create your views here.
def index(request):
    return render(request, "distance/index.html", {
        "distances": Distance.objects.all()
    })

def distance( request, distance_id):
    distance = Distance.objects.get(pk=distance_id)
    return render(request, "distance/distances.html", {
        "distance": distance
    })

def log(request):
    if request.method == 'GET':
        context = {'form': LogForm()}
        return render(request, "distance/log.html", context)
    elif request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, "distance/log.html", {'form': form})

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

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'distance/register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration successful. Welcome to the competition!')
            login(request, user)
            return redirect('log')
        else:
            return render(request, 'distance/register.html', {'form': form})