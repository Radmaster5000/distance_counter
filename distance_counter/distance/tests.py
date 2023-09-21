from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Distance, Person, Office

class IndexViewTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view_for_logged_in_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create some Distance objects in the database
        Distance.objects.create(date='2023-09-15', person=self.user.person, distance=10.5, unit='km')
        Distance.objects.create(date='2023-09-16', person=self.user.person, distance=15.0, unit='km')

        # Use the Client to simulate a GET request to the index page
        response = self.client.get(reverse('index'))

        # Check if the response contains the expected content and status code
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2023-09-15')
        self.assertContains(response, '2023-09-16')

    def test_index_view_for_anonymous_user(self):
        # Use the Client to simulate a GET request to the index page
        response = self.client.get(reverse('index'))

        # Check if the response redirects to the login page (status code 302)
        self.assertEqual(response.status_code, 302)

        # Check if the response redirects to the login page URL (name 'login')
        self.assertRedirects(response, reverse('login'))

class DistanceViewTestCase(TestCase):
    def setUp(self):
        # Create an Office instance
        office = Office.objects.create(
            city="Your City",
            country="Your Country"
        )

        # Create a Person instance
        self.person = Person.objects.create(
            first_name="Philip",
            last_name="Radford",
            email="philip@example.com",
            location=office  # Replace with a valid Office instance
        )
        # Create a Distance object in the database for testing
        self.distance = Distance.objects.create(
            date="2023-09-15",
            person="Philip, Radford",  # Replace with an actual Person object or create one
            distance=10.5,  # Replace with an actual distance value
            unit="km"  # Replace with an actual Unit object or create one
        )

    def test_distance_view_for_existing_distance(self):
        # Use the Client to simulate a GET request to the distance detail page
        response = self.client.get(reverse('distance', args=[self.distance.id]))

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected content (e.g., distance details)
        self.assertContains(response, f"Distance ID: {self.distance.id}")
        self.assertContains(response, f"Date: {self.distance.date}")
        self.assertContains(response, f"Person: {self.distance.person}")
        self.assertContains(response, f"Distance: {self.distance.distance} {self.distance.unit}")

    def test_distance_view_for_non_existing_distance(self):
        # Use the Client to simulate a GET request to a non-existing distance detail page
        response = self.client.get(reverse('distance', args=[999]))  # Using an invalid distance ID

        # Check if the response has a status code of 404 (Not Found)
        self.assertEqual(response.status_code, 404)


class LogViewTestCase(TestCase):
    def setUp(self):

        # Create an Office instance
        office = Office.objects.create(
            city="Your City",
            country="Your Country"
        )
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Create a Person instance
        self.person = Person.objects.create(
            first_name="Philip",
            last_name="Radford",
            email="philip@example.com",
            location=office  # Replace with a valid Office instance
        )

    def test_log_view_for_get_request(self):
        # Use the Client to simulate a GET request to the log page
        response = self.client.get(reverse('log'))

        # Check if the response contains the expected form and has a 200 status code
        self.assertEqual(response.status_code, 200)
        print(response)
        self.assertContains(response, '<HttpResponse status_code=200', html=True)  # Assuming there's an HTML form on the page

    def test_log_view_for_post_request_with_valid_data(self):
        # Use the Client to simulate a POST request to log a distance with valid data
        data = {
            'date': '2023-09-15',
            'person': self.person,  # Assuming the user is the person
            'distance': '10.5',
            'unit': 'miles',
        }
        response = self.client.post(reverse('log'), data)

        # Check if the response redirects to the index page (assuming a successful log)
        self.assertRedirects(response, reverse('index'))

    def test_log_view_for_post_request_with_invalid_data(self):
        # Use the Client to simulate a POST request to log a distance with invalid data
        data = {
            'date': '',  # Invalid: Date is required
            'person': self.person,
            'distance': '',  # Invalid: Distance is required
            'unit': 'miles',
        }
        response = self.client.post(reverse('log'), data)

        # Check if the response contains errors and stays on the log page
        self.assertEqual(response.status_code, 200)  # Should stay on the page
        self.assertContains(response, 'This field is required.', html=True)  # Example error message


