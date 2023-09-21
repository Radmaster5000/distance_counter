from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, LogForm, OfficeForm, PersonForm, UnitForm, LogForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Distance, Person, Office, Unit

# Create your views here.

def index(request):
    """
    Displays all of the distance records for logged-in users

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered index page.
    """
    return render(request, "distance/index.html", {
        "distances": Distance.objects.all()
    })

@login_required

def distance( request, distance_id):
    """
    Displays the details of a specific distance record

    Args:
        request (HttpRequest): The HTTP request object
        distance_id (int): The ID of the distance record to display

    Returns:
        HttpResponse: The rendered distance detail page
    """
    distance = Distance.objects.get(pk=distance_id)
    return render(request, "distance/distances.html", {
        "distance": distance
    })

@login_required
def log(request):
    """
    Handles both GET and POST requests for distance logging

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered distance logging page
    """
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
    """
    Handles both GET and POST requests for user login

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered login page or a redirection to the log page on successful login
    """
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
            
        # form isn't valid or the user's unauthenticated
        messages.error(request, f"Invalid username or password, please try again!")
        return render(request, 'distance/login.html', {'form': form})

   
def sign_out(request):
    """
    Logs the user out and displays a confirmation message

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: A redirection to the login page after logout
    """
    logout(request)
    messages.success(request, f"You're now logged out. Why are you logging out?")
    return redirect('login')


def register(request):
    """
    Handles both GET and POST requests for user registration

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered registration page or a redirection to the log page on successful registration
    """
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
    """
    Handles both GET and POST requests for creating a new office location

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered office creation page or a redirection to the index page on successful creation
    """
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OfficeForm()
    return render(request, 'distance/create.html', {'form': form})

@login_required
def person_create(request):
    """
    Handles both GET and POST requests for creating a person

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered person creation page or a redirection to the index page on successful creation
    """
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PersonForm()
    return render(request, 'distance/create.html', {'form': form})

@login_required
def unit_create(request):
    """
    Handles both GET and POST requests for creating a new unit of measurement

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered unit creation page or a redirection to the index page on successful creation
    """
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UnitForm()
    return render(request, 'distance/create.html', {'form': form})

@login_required
def log_create(request):
    """
    Handles both GET and POST requests for creating a new log

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered log creation page or a redirection to the index page on successful creation
    """
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = LogForm()
    return render(request, 'distance/create.html', {'form': form})

@login_required
def distance_edit(request, distance_id):
    """
    Handles both GET and POST requests for editing a distance record

    Args:
        request (HttpRequest): The HTTP request object
        distance_id (int): The ID of the distance record to edit

    Returns:
        HttpResponse: The rendered distance editing page or a redirection to the distance detail page on successful edit
    """
    distance = get_object_or_404(Distance, pk=distance_id)

    if request.method == 'POST':
        form = LogForm(request.POST, instance=distance)
        if form.is_valid():
            form.save()
            return redirect('distance', distance_id=distance_id)

    else:
        form = LogForm(instance=distance)

    return render(request, 'distance/edit.html', {'form': form, 'distance': distance})

@login_required
def delete_distance(request, distance_id):
    """
    Handles the deletion of a specific distance record when a POST request is received
    After successful deletion, it redirects the user to the index page

    Args:
        request (HttpRequest): The HTTP request object
        distance_id (int): ID of the distance record to delete

    Returns:
        HttpResponse: A redirection to the index page or the distance detail page based on the request
    """
    distance = get_object_or_404(Distance, pk=distance_id)
    
    if request.method == 'POST':
        distance.delete()
        return redirect('index')  
    return redirect('distance', distance_id=distance_id)  

@login_required
def people(request):
    """
    Retrieves all person records from the database and renders a page
    displaying the list of people along with their details

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered people list page
    """
    people = Person.objects.all()
    return render(request, "distance/people.html", {
        "persons": people   
    })

@login_required
def person( request, person_id):
    """
    Retrieves a specific person record from the database based on the provided
    person_id and renders a page displaying the details of that person

    Args:
        request (HttpRequest): The HTTP request object
        person_id (int): The ID of the person record to display

    Returns:
        HttpResponse: The rendered person details page
    """
    person = Person.objects.get(pk=person_id)
    return render(request, "distance/person.html", {
        "person": person
    })

@login_required
def person_edit(request, person_id):
    """
    Handles both GET and POST requests for editing a person

    Args:
        request (HttpRequest): The HTTP request object
        person_id (int): The ID of the person to edit

    Returns:
        HttpResponse: The rendered person editing page or a redirection to the person detail page on successful edit
    """
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person', person_id=person_id)

    else:
        form = PersonForm(instance=person)

    return render(request, 'distance/edit.html', {'form': form, 'person': person})

@login_required
def delete_person(request, person_id):
    """
    Handles the deletion of a specific person when a POST request is received
    After successful deletion, it redirects the user to the index page

    Args:
        request (HttpRequest): The HTTP request object
        person_id (int): ID of the person to delete

    Returns:
        HttpResponse: A redirection to the index page or the person detail page based on the request
    """
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        person.delete()
        return redirect('people') 
    return redirect('person', person_id=person_id) 

@login_required
def offices(request):
    """
    Retrieves all office records from the database and renders a page
    displaying the list of offices along with their location

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered offices list page
    """
    offices = Office.objects.all()
    return render(request, "distance/offices.html", {
        "offices": offices  
    })

@login_required
def office( request, office_id):
    """
    Retrieves a specific office record from the database based on the provided
    office_id and renders a page displaying the name and location of that office

    Args:
        request (HttpRequest): The HTTP request object
        office_id (int): The ID of the office record to display

    Returns:
        HttpResponse: The rendered office details page
    """
    office = Office.objects.get(pk=office_id)
    return render(request, "distance/office.html", {
        "office": office
    })

@login_required
def office_edit(request, office_id):
    """
    Handles both GET and POST requests for editing an office

    Args:
        request (HttpRequest): The HTTP request object
        office_id (int): The ID of the office record to edit

    Returns:
        HttpResponse: The rendered office editing page or a redirection to the office detail page on successful edit
    """
    office = get_object_or_404(Office, pk=office_id)

    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect('office', office_id=office_id)

    else:
        form = OfficeForm(instance=office)

    return render(request, 'distance/edit.html', {'form': form, 'office': office})

@login_required
def delete_office(request, office_id):
    """
    Handles the deletion of a specific office when a POST request is received
    After successful deletion, it redirects the user to the index page

    Args:
        request (HttpRequest): The HTTP request object
        office_id (int): ID of the office to delete

    Returns:
        HttpResponse: A redirection to the index page or the office detail page based on the request
    """
    office = get_object_or_404(Office, pk=office_id)

    if request.method == 'POST':
        office.delete()
        return redirect('offices') 
    return redirect('office', office_id=office_id) 

@login_required
def units(request):
    """
    Retrieves all unit of measurement records from the database and renders a page
    displaying the list of units

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: The rendered units list page
    """
    units = Unit.objects.all()
    return render(request, "distance/units.html", {
        "units": units  
    })

@login_required
def unit( request, unit_id):
    """
    Retrieves a specific unit from the database based on the provided
    unit_id and renders a page displaying the details of that unit of measurement

    Args:
        request (HttpRequest): The HTTP request object
        unit_id (int): The ID of the unit record to display

    Returns:
        HttpResponse: The rendered unit details page
    """
    unit = Unit.objects.get(pk=unit_id)
    return render(request, "distance/unit.html", {
        "unit": unit
    })

@login_required
def unit_edit(request, unit_id):
    """
    Handles both GET and POST requests for editing a unit of measurement

    Args:
        request (HttpRequest): The HTTP request object
        unit_id (int): The ID of the unit record to edit

    Returns:
        HttpResponse: The rendered unit editing page or a redirection to the unit detail page on successful edit
    """
    unit = get_object_or_404(Unit, pk=unit_id)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit', unit_id=unit_id)

    else:
        form = UnitForm(instance=unit)

    return render(request, 'distance/edit.html', {'form': form, 'unit': unit})

@login_required
def delete_unit(request, unit_id):
    """
    Handles the deletion of a specific unit of measurement when a POST request is received
    After successful deletion, it redirects the user to the index page

    Args:
        request (HttpRequest): The HTTP request object
        unit_id (int): ID of the unit to delete

    Returns:
        HttpResponse: A redirection to the index page or the unit detail page based on the request
    """
    unit = get_object_or_404(Unit, pk=unit_id)

    if request.method == 'POST':
        unit.delete()
        return redirect('units') 
    return redirect('unit', unit_id=unit_id) 