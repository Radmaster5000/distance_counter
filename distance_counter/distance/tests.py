from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Distance, Person, Office, Unit

class IndexViewTestCase(TestCase):
    def setUp(self):
        # Creates a new user for testing, and a Person and some Distance data for the database

        office = Office.objects.create(
            city="City",
            country="Country"
        )

        self.person = Person.objects.create(
            first_name="Philip",
            last_name="Radford",
            email="philip@example.com",
            location=office 
        )

        #Create a Unit instance
        self.unit = Unit.objects.create(
            unit_of_measurement = "steps"
        )

        Distance.objects.create(date='2023-09-15', person=self.person, distance=10.5, unit=self.unit)
        Distance.objects.create(date='2023-09-16', person=self.person, distance=15.0, unit=self.unit)

    def test_index_view_for_anonymous_user(self):
        # Send a GET request to the index page
        response = self.client.get(reverse('index'))

        # Check if the response is okay
        self.assertEqual(response.status_code, 200)

        # Check if the response contains a message to log in first
        self.assertIn("Please log in to view this content.", str(response.content))

    def test_index_view_for_logged_in_user(self):
        self.user = User.objects.create_user(username='user', password='password')
        # Log the user in 
        self.client.login(username='user', password='password')

        # Send a GET request to the index page
        response = self.client.get(reverse('index'))

        # Check if the response contains the expected content and status code
        self.assertEqual(response.status_code, 200)

        self.assertIn("Sept. 15, 2023", str(response.content))
        self.assertIn("Sept. 16, 2023", str(response.content))

class DistanceViewTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='user', password='password')
        # Create an Office instance
        office = Office.objects.create(
            city="Manchester",
            country="UK"
        )

        # Create a Person instance
        self.person = Person.objects.create(
            first_name="Homer",
            last_name="Simpson",
            email="Homer@simpsons.com",
            location=office  
        )

        #Create a Unit instance
        self.unit = Unit.objects.create(
            unit_of_measurement = "steps"
        )

        # Create a Distance object in the database for testing
        self.distance = Distance.objects.create(
            id = 1337,
            date="2023-09-15",
            person=self.person, 
            distance=10.5,
            unit=self.unit
        )

    def test_distance_view_for_existing_distance(self):
        self.client.login(username='user', password='password')
        # Use the Client to simulate a GET request to the distance detail page
        response = self.client.get(reverse('distance', args=[self.distance.id]))

        # Check if the response has a status code of 200
        self.assertEqual(response.status_code, 200)


        self.assertContains(response, f"{self.distance.person}")
        self.assertIn("Sept. 15, 2023", str(response.content))
        self.assertIn("10.5", str(response.content))
        self.assertIn("steps", str(response.content))


    def test_distance_view_for_non_existing_distance(self):

        self.client.login(username='user', password='password')

        # Send a GET request with an invalid distance detail page
        response = self.client.get(reverse('distance', args=[999])) 

        # Check if the response has a Not Found status code
        self.assertEqual(response.status_code, 404)


class LogViewTestCase(TestCase):
    def setUp(self):

        # Create an Office instance
        office = Office.objects.create(
            city="Cambridge",
            country="UK"
        )

        #Create a Unit instance
        self.unit = Unit.objects.create(
            id = 13,
            unit_of_measurement = "Miles"
        )

        # Creating a user and logging them in
        self.user = User.objects.create_user(username='new', password='secret')
        self.client.login(username='new', password='secret')

        # Create a Person instance
        self.person = Person.objects.create(
            first_name="Marge",
            last_name="Simpson",
            email="Marge.Simpson@example.com",
            location=office
        )

        self.distance = Distance.objects.create(
            date="2023-09-15",
            person=self.person, 
            distance=10.5,
            unit=self.unit
        )

    def test_log_view_for_get_request(self):
        self.client.login(username='user', password='password')
        # Send a GET request to the log page
        response = self.client.get(reverse('log'))

        # Check if the response contains the expected form and has a 200 status code
        self.assertEqual(response.status_code, 200)


    def test_log_view_for_post_request_with_valid_data(self):
        # Send a POST request to log a distance with valid data
        data = {
            'date': '2023-09-15',
            'person': self.person,  # Assuming the user is the person
            'distance': '10.5',
            'unit': self.unit,
        }
        response = self.client.post(reverse('log'), data)

        # Check if the response redirects to the index page (assuming a successful log)
        # self.assertRedirects(response, reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_log_view_for_post_request_with_invalid_data(self):
        # Send a POST request to log a distance with missing data
        data = {
            'date': '',  
            'person': self.person,
            'distance': '',  
            'unit': 'miles',
        }
        response = self.client.post(reverse('log'), data)

        # Check if the response contains errors and stays on the log page
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'This field is required.', html=True)  

class UnitViewTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='user', password='password')

        #Create a Unit instance
        self.unit = Unit.objects.create(
            id = 123,
            unit_of_measurement = "steps"
        )


    def test_unit_view_for_existing_unit(self):
        self.client.login(username='user', password='password')
        # Use the Client to simulate a GET request to the unit detail page
        response = self.client.get(reverse('unit', args=[self.unit.id]))

        # Check if the response contains the expected form and has a 200 status code
        self.assertEqual(response.status_code, 200)

    def test_post_to_unit(self):
        self.client.login(username='user', password='password')
        data = {
            'unit': 'lightyears'
        }

        response = self.client.post(reverse('unit_create'), data)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)



    def test_delete_unit(self):
        self.client.login(username='user', password='password')
        #Create a Unit instance
        self.unit = Unit.objects.create(
            id = 13,
            unit_of_measurement = "Miles"
        )

        response = self.client.get(reverse('delete_unit', args=[self.unit.id]))

        # Check if the response redirects the user due to the unit no longer existing
        self.assertEqual(response.status_code, 302)


class PersonViewTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='user', password='password')

        # Create an Office instance
        self.office = Office.objects.create(
            city="Springfield",
            country="USA"
        )

        #Create a Person instance
        self.person = Person.objects.create(
            id = 123,
            first_name = "Marge",
            last_name = "Simpson",
            email = "Marge.Simpson@example.com",
            location = self.office
        )


    def test_person_view_for_existing_person(self):
        self.client.login(username='user', password='password')
        # Use the Client to simulate a GET request to the person detail page
        response = self.client.get(reverse('person', args=[self.person.id]))

        # Check if the response contains the expected form and has a 200 status code
        self.assertEqual(response.status_code, 200)

    def test_post_to_person(self):
        self.client.login(username='user', password='password')
        
        data = {
            'first_name':"Marge",
            "last_name":"Simpson",
            "email":"Marge.Simpson@example.com",
            "location":"Springfield"
        }



        response = self.client.post(reverse('person_create'), data)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)



    def test_delete_person(self):
        self.client.login(username='user', password='password')

        response = self.client.get(reverse('delete_person', args=[self.person.id]))

        # Check if the response redirects the user due to the person no longer existing
        self.assertEqual(response.status_code, 302)

class OfficeViewTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='user', password='password')

        #Create a Office instance
        self.office = Office.objects.create(
            id = 123,
            city = "Night City",
            country = "USA"
        )


    def test_office_view_for_existing_office(self):
        self.client.login(username='user', password='password')
        # Use the Client to simulate a GET request to the office detail page
        response = self.client.get(reverse('office', args=[self.office.id]))

        # Check if the response contains the expected form and has a 200 status code
        self.assertEqual(response.status_code, 200)

    def test_post_to_office(self):
        self.client.login(username='user', password='password')
        data = {
            "city":"Night City",
            "country":"USA"
        }

        response = self.client.post(reverse('office_create'), data)

        # Check if user is redirected if request is successful
        self.assertEqual(response.status_code, 302)



    def test_delete_office(self):
        self.client.login(username='user', password='password')

        response = self.client.get(reverse('delete_office', args=[self.office.id]))

        # Check if the response redirects the user due to the Office no longer existing
        self.assertEqual(response.status_code, 302)