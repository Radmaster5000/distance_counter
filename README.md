# distance_counter
distance_counter for SWE Level 5

# Usage
- Clone the repo
- Create a virtual environment
- Install requirements.txt
- from /distance_counter/distance_counter run `python manage.py runserver`

This will run the page from http://127.0.0.1:8000 which will return an error.
The 'homepage' is currently as above with /distance added to the end, so http://127.0.0.1:8000/distance

Alternatively use http://127.0.0.1:8000/admin for the Admin View

Login page works, and new users can register themselves.

Database created and ready to be populated.

Index page now shows all current logs, and each log is a link to an 
individual page for that log

Log page now takes data and saves it to the database

Still looks awful.