from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, LogForm, OfficeForm, PersonForm, UnitForm, LogForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Distance, Person, Office, Unit

# Create your views here.
@login_required
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
        # Getting all the users from the users table to populate the selectable
        # people in the 'Person' dropdown
        users = User.objects.all()
        person_options = [(user.id, user.username) for user in users]
        form = LogForm(initial={'person': person_options})
        context = {'form': form}
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
        
@login_required        
def office_create(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OfficeForm()
    return render(request, 'distance/create.html', {'form': form})

def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PersonForm()
    return render(request, 'distance/create.html', {'form': form})

def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UnitForm()
    return render(request, 'distance/create.html', {'form': form})

def log_create(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = LogForm()
    return render(request, 'distance/create.html', {'form': form})

def distance_edit(request, distance_id):
    distance = get_object_or_404(Distance, pk=distance_id)

    if request.method == 'POST':
        form = LogForm(request.POST, instance=distance)
        if form.is_valid():
            form.save()
            return redirect('distance', distance_id=distance_id)

    else:
        form = LogForm(instance=distance)

    return render(request, 'distance/edit.html', {'form': form, 'distance': distance})

def delete_distance(request, distance_id):
    distance = get_object_or_404(Distance, pk=distance_id)
    
    if request.method == 'POST':
        distance.delete()
        return redirect('index')  
    return redirect('distance', distance_id=distance_id)  

def people(request):
    people = Person.objects.all()
    return render(request, "distance/people.html", {
        "persons": people   
    })

def person( request, person_id):
    person = Person.objects.get(pk=person_id)
    return render(request, "distance/person.html", {
        "person": person
    })

def person_edit(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person', person_id=person_id)

    else:
        form = PersonForm(instance=person)

    return render(request, 'distance/edit.html', {'form': form, 'person': person})

def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        person.delete()
        return redirect('people') 
    return redirect('person', person_id=person_id) 

def offices(request):
    offices = Office.objects.all()
    return render(request, "distance/offices.html", {
        "offices": offices  
    })

def office( request, office_id):
    office = Office.objects.get(pk=office_id)
    return render(request, "distance/office.html", {
        "office": office
    })

def office_edit(request, office_id):
    office = get_object_or_404(Office, pk=office_id)

    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect('office', office_id=office_id)

    else:
        form = OfficeForm(instance=office)

    return render(request, 'distance/edit.html', {'form': form, 'office': office})

def delete_office(request, office_id):
    office = get_object_or_404(Office, pk=office_id)

    if request.method == 'POST':
        office.delete()
        return redirect('offices') 
    return redirect('office', office_id=office_id) 

def units(request):
    units = Unit.objects.all()
    return render(request, "distance/units.html", {
        "units": units  
    })

def unit( request, unit_id):
    unit = Unit.objects.get(pk=unit_id)
    return render(request, "distance/unit.html", {
        "unit": unit
    })

def unit_edit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit', unit_id=unit_id)

    else:
        form = UnitForm(instance=unit)

    return render(request, 'distance/edit.html', {'form': form, 'unit': unit})

def delete_unit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)

    if request.method == 'POST':
        unit.delete()
        return redirect('units') 
    return redirect('unit', unit_id=unit_id) 

def custom_404(request, exception):
    return render(request, '404.html', status=404)