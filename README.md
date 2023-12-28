# Modern Class

A Live Demo: [Modern CLASS DEMO](https://modernclass.pythonanywhere.com)

The modern class is a my CS50W's Final Project an it's a web app belongs to a bigger project called Modern School and the Modern Class's purpose is to spread knowledge by easing the connection between students and teachers.

it was built with django, javascript, CSS, TailwindCSS, HTML and Sqlite3.

# Distinctiveness and Complexity
Modern Class as an idea is obviously distinctive from the CS50W course projects and as a code it uses the TailwindCSS framework (not Bootstrap) and it's mobile responsive and the code generally is more complex in terms of linking the models in the database and the challenging views and javascript functions that were written.

# Structure
## Files
- **layout.html**: the main structure.
- **register.html**: it has the register form.
- **login.html**: the page for login a pre registered user.
- **index.html**: the main page of website it lists all the courses for all users with some differences for authenticated users and between teachers and students as well.
- **class.html**: is the Class Page and it's of course different for each class and for different types of users.
- **create.html**: this page is only available for teachers and it has a form creating a new class.
- **error.htnl**: a well designed 404 error page.
- **index.js**: has all the javascript functionality that *index.html* needs.
- **class.js**: has all the javascript functionality that *class.html* needs.
- **styles.css**: has all the custom css needed for the app.
## Models
- **User**: extends the AbstractUser Class and add a full_name (CHAR) and is_teacher (boolean) fields.
- **Classroom**: it represents the classroom or class for short (but it's a reserved word in python).
- **Content**: represents the class content.

# Installations and Usage
first run the following command to install all requirements:

`pip install -r requirements.txt`

and then go to the directory of the `manage.py` file and run:

`python manage.py migrate` to build your database

and then run `python manage.py createsuperuser` to create and admin user for you and finally run `python manage.py runserver` to start the app.

**NOTES**:
- you'll encounter the `DisallowedHost` Error and to solve it add the the header it tells you about to `ALLOWED_HOSTS` list in `mschool/settings.py`

- if you encountered a CSRF trust error then add your whole domain link (including https/http) to the `CSRF_TRUSTED_ORIGINS` list in the `mschool/settings.py` file.

- if you would like to use the Django-Debug-Toolbar utility then make sure that the `DEBUG` variable is set to True in your `mschool/settings.py` file and add your localhost/server ip to the `INTERNAL_IPS` list in that same file.

<hr>
