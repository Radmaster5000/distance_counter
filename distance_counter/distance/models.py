from django.db import models

# Create your models here.

class Office(models.Model):
    """Office location

    Stores information about office locations, including the city and country

    Attributes:
        city (str): Name of the city where the office is located
        country (str): Name of the country where the office is located

    Methods:
        __str__: Returns a string representation of the office

    """
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}"

class Person(models.Model):
    """For creating people

    Stores information about a person, including their first name, last name, email,
    and their associated office location

    Attributes:
        first_name (str): First name of the person
        last_name (str): Last name of the person
        email (str): Email address of the person
        location (Office): Office location where the person works (foreign key)

    Methods:
        __str__: Returns a string representation of the person

    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"

class Unit(models.Model):
    """Units of measurement

    Stores information about a unit of measurement

    Attributes:
        unit_of_measurement (str): Name/symbol representing the unit of measurement

    Methods:
        __str__: Returns a string representation of the unit

    """
    unit_of_measurement = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.unit_of_measurement}"

class Distance(models.Model):
    """Creates Distances

    Stores information about a recorded distance, including the date it was recorded,
    the person who recorded it, the distance value, and the unit of measurement used

    Attributes:
        date (Date): Date the distance was recorded in YYYY-MM-DD format
        person (Person): The person who recorded the distance (foreign key)
        distance (Decimal): The recorded distance value
        unit (Unit): The unit of measurement used for the distance (foreign key)

    Methods:
        __str__: Returns a string representation of the distance entry in the format
                  "Date: Last Name, First Name"

    """
    date = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.person.last_name}, {self.person.first_name}"

