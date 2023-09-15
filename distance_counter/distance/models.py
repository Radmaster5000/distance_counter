from django.db import models

# Create your models here.

class Office(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}"

class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"

class Unit(models.Model):
    unit_of_measurement = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.unit_of_measurement}"

class Distance(models.Model):
    date = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.person.last_name}, {self.person.first_name}"

