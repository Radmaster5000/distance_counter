# distance_counter
distance_counter for SWE Level 5


# Overview

The purpose of this application is to log data with regards to Arm's annual movement challenge. Every year a target distance is set for the company to achieve as a common goal by; running, walking, hiking, swimming, etc. This application lets users upload their movements to create a record that can be revisited at any time. Anyone can create an account, however Admin privileges must be given by an existing Admin (known as a SuperUser in the Django framework). 

Users can log their own, or another person's distances by clicking 'Record Distance' on the navigation bar at the top of the screen.
To log a distance, the user is required to input;
- a date (in YYYY-MM-DD format)
- A person (selectable from the available dropdown)
- A distance (Any number including up to two decimal places)
- A unit of measurement (selectable from the available dropdown)

If the dropdown menus do not contain a required record, new ones can be created using the 'Create' dropdown menu on the navigation bar at the top of the screen.

The 'View' dropdown menu on the navigation bar at the top of the page allows the user to view records from the different tables; First taking them to a view of all of the tables' records and then to individual records by selecting the individual link in the first column of the table. 

Individual records will give a regular user the option to edit the record, and a Superuser or Admin the options to edit and delete the record.
# Usage
- Clone the repo
- Create and start a virtual environment
- Install requirements.txt
- from /distance_counter/distance_counter run `python manage.py runserver`

The website can then be accessed by visiting http://127.0.0.1:8000/distance

Alternatively, Superusers can use http://127.0.0.1:8000/admin for the Admin View


# Testing

Testing uses Django's Test framework and unit tests can be executed by running `python manage.py test distance` from the directory that contains `manage.py`
There are currently 16 unit tests that test the different views' functionality.
# Database structure/Models used

- OFFICE: City and Country of office locations. Includes `city`, and `country`
- PERSON: The person who has undertook the activity. Includes `first_name`, `last_name`, `email_address`, and  `location`. `location` is a foreign key, originating from the OFFICE table
- UNIT: The `unit of measurement` used for logging (steps taken, miles travelled)
- DISTANCE: Each record includes `date` (format is YYYY-MM-DD), `person` (foreign key, originating from PERSON table), `distance`, and `unit` (foreign key, originating from UNIT table) 

If a DISTANCE is being created that requires a new PERSON, the dependencies go DISTANCE > PERSON > LOCATION. So if the new PERSON works at a new LOCATION, the LOCATION record must be created first, then the PERSON record, then the DISTANCE record.
