# Modern Class

A live demo of the project can be found here: [Modern CLASS DEMO](https://modernclass.pythonanywhere.com)

The Modern Class is my final project for CS50W. It is a web application that is part of a larger project known as Modern School. The primary aim of Modern Class is to facilitate knowledge sharing by simplifying the connection between students and teachers.

The application was built using Django, JavaScript, CSS, TailwindCSS, HTML, and SQLite3.

## Distinctiveness and Complexity

The Modern Class project differs from other CS50W course projects due to its unique concept and distinctive execution. The code uses the TailwindCSS framework instead of Bootstrap to make it mobile responsive and give it an aesthetic taste different from other previous projects. Additionally, the code is more complex due to the intricate model linking in the database and the challenging views and JavaScript functions that were written.

One key feature of this project is the use of the Django Debug Toolbar, a powerful tool for developing Django project and Troubleshooting hidden or abvious bugs. This tool was not covered in any previous problem sets of the course and its use demonstrates the application's complexity and the new skills that were acquired.

Another distinguishing factor is the use of the image fields in the database. This feature allows the storage and retrieval of images directly within the database, adding another layer of complexity to the application. And as well this feature wasn't covered in any previous problem sets which highlights the distinctiveness of this project.


## File Structure

### Files

#### Frontend
- **layout.html**: This is the main structure of the application.
- **register.html**: This file contains the registration form.
- **login.html**: This page is used for logging in a pre-registered user.
- **index.html**: This is the main page of the website, listing all the courses for all users. The display varies for authenticated users and between teachers and students.
- **class.html**: This is the Class Page, which differs for each class and for different types of users.
- **create.html**: This page is accessible only to teachers and contains a form for creating a new class.
- **error.html**: This is a well-designed 404 error page.
- **index.js**: This file contains all the JavaScript functionality required by *index.html*.
- **class.js**: This file contains all the JavaScript functionality required by *class.html*.
- **styles.css**: This file contains all the custom CSS required for the app.

#### Backend
- **views.py**: This file contains all the view functions that process incoming requests and return the appropriate responses.
- **utils.py**: This file contains helper functions such as the image validation function.
- **urls.py**: This file routes different URL calls to the corresponding view functions.
- **admin.py**: This file configures the administrative interface for the app.
- **models.py**: This file defines the data structures used in the app, including User, Classroom, and Content models.
- **settings.py**: This file contains settings for the Django application, including configuration for allowed hosts, CSRF trusted origins, and debug mode.

### Models
- **User**: This model extends the AbstractUser Class and adds a full_name (CHAR) and is_teacher (boolean) field.
- **Classroom**: This model represents the classroom.
- **Content**: This model represents the class content.

## Installation and Usage

- First run the following command to install all requirements: `pip install -r requirements.txt`

- And then go to the directory of the `manage.py` file and run: `python manage.py migrate` to build your database

- And then run `python manage.py createsuperuser` to create and admin user for you and finally run `python manage.py runserver` to start the app.

**NOTES**:
- You'll encounter the `DisallowedHost` Error and to solve it add the the header it tells you about to `ALLOWED_HOSTS` list in `mschool/settings.py`

- If you encountered a CSRF trust error then add your whole domain link (including https/http) to the `CSRF_TRUSTED_ORIGINS` list in the `mschool/settings.py` file.

- If you would like to use the Django-Debug-Toolbar utility then make sure that the `DEBUG` variable is set to True in your `mschool/settings.py` file and add your localhost/server ip to the `INTERNAL_IPS` list in that same file.

<hr>
