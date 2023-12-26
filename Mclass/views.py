import json
from .utils import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Classroom, Content

# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return error_404(request)
    if request.method == "POST":
        full_name = request.POST["full-name"]
        email = request.POST["email"]
        role = request.POST["role"]
        is_teacher = True if role == "teacher" else False

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm-password"]
        if password != confirmation:
            return render(request, "Mclass/register.html",
                          {"message": "Passwords must match."})

        # make sure that fields are not left empty
        if not password or not confirmation or not email or not full_name:
            return render(request, "Mclass/register.html",
                          {"message": "All Fields Are Required."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(email.lower(),
                                            password=password,
                                            full_name=full_name,
                                            is_teacher=is_teacher)
            user.save()
        except IntegrityError:
            return render(request, "Mclass/register.html",
                          {"message": "Email Already Has an Account"})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Mclass/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return error_404(request)
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email.lower(), password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Mclass/login.html",
                          {"message": "Invalid email and/or password."})
    else:
        return render(request, "Mclass/login.html")


# logout the user
def logout_view(request):
    if not request.user.is_authenticated:
        return error_404(request)
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# the main view
def index(request):
    if request.method == "POST":
        data = json.loads(request.body)
        filter = data["filter"]
        page = data["page"]
        classes = None

        if filter == "all":
            classes = Classroom.objects.all()

        # the student their enrolled classes and the teacher thier own classes
        elif filter == "my":
            if request.user.is_teacher:
                classes = request.user.tclass.all()
            else:
                classes = request.user.sclass.all()

        # show classes as the filter was set
        elif filter == "filter":
            kargs = dict()
            if data["category"] != '':

                kargs["category"] = data["category"]
            if data["type"] != '':
                kargs["private"] = True if data["type"] == "private" else False
            if data["availability"] != '':
                kargs["closed"] = True if data[
                    "availability"] == "closed" else False

            classes = Classroom.objects.filter(**kargs)

        # show classes that contain the search keyword in their title or the details or teacher name
        elif filter == "search":
            sw = data["search_word"]
            classes = Classroom.objects.filter(title__contains=sw) | (
                Classroom.objects.filter(details__contains=sw)) | (
                    Classroom.objects.filter(teacher__full_name__contains=sw))

        else:
            return error_404()

        # make a list of dictionaries of classes
        classes_list = [c.serialize() for c in classes]

        # sort depending on ids
        sorted_classes = sorted(classes_list,
                                key=lambda _: _['id'],
                                reverse=True)

        # make a paginator
        pg = Paginator(sorted_classes, 10)
        try:
            p = pg.page(page)
        except EmptyPage:
            return error_404(request)

        #return a json response
        return JsonResponse(
            {
                "has_next": p.has_next(),
                "has_previous": p.has_previous(),
                "num_pages": pg.num_pages,
                "classes": p.object_list,
            },
            status=201)
    return render(request, 'Mclass/index.html')


# create a new class
def create_view(request):
    user = request.user
    if not user.is_authenticated and not user.is_teacher:
        return error_404(request)

    if request.method == "POST":
        data = request.POST

        kargs = {
            'private': True,
            'title': data.get('title'),
            'category': data.get('category'),
            'details': data.get('details'),
            'teacher': request.user,
            'private': False if data.get('visibility') == "public" else False,
        }

        image = data.get('image')
        if image != '':
            if not image_is_valid(image):
                return render(request, "Mclass/create.html", {
                    "message": "Invalid Image URL",
                    "options": get_options()
                })

            kargs['image'] = image

        classroom = Classroom(**kargs)
        classroom.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "Mclass/create.html", {"options": get_options()})

# create a new class
def class_settings(request, id):
    user = request.user
    if not user.is_authenticated and not user.is_teacher and request.method != "POST":
        return error_404(request)

    data = request.POST
    class_object = Classroom.objects.filter(id=id)
    print(data.get('category'))

    kargs = {
        'private': True if data.get('visibility') == 'private' else False,
        'category': data.get('category'),
        'closed': True if data.get('availability') == "closed" else False,
    }

    class_object.update(**kargs)
    request.method = "GET"
    return redirect('class_view', class_id=id, title=class_object.first().title)


# the class view
def class_view(request, class_id, title=""):
    class_object = Classroom.objects.get(id=class_id)
    # enroll students to a class
    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_teacher:
            if request.user not in class_object.student.all():
                if class_object.private:
                    if request.user not in class_object.request.all():
                        class_object.request.add(request.user)
                    else:
                        class_object.request.remove(request.user)
                else:
                    class_object.student.add(request.user)
            else:
                class_object.student.remove(request.user)
        else:
            return error_404(request)
    return render(
        request, "Mclass/class.html", {
            "data": class_object.serialize(),
            "teacher": class_object.teacher,
            "options": get_options()
        })


# removing a student from a class
@login_required
def kick_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        classroom = Classroom.objects.get(id=data["class_id"])
        if request.user != classroom.teacher:
            return error_404(request)
        student = User.objects.get(id=data["student_id"])
        classroom.student.remove(student)
        return JsonResponse({}, status=201)
    return error_404(request)


# list students or requests
def list_students(request, type):
    if request.method == "POST":
        if not request.user.is_authenticated or not request.user.is_teacher:
            return error_404(request)

        data = json.loads(request.body)
        classroom = Classroom.objects.get(id=data["id"])

        if classroom.teacher != request.user:
            return error_404(request)

        if type == "s":
            items = classroom.student.all()
        else:
            items = classroom.request.all()

        return JsonResponse(
            {"students": [{
                "name": s.full_name,
                "id": s.id
            } for s in items]},
            status=201)
    return error_404(request)


@login_required
def edit_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student = User.objects.get(id=data["student_id"])
        classroom = Classroom.objects.get(id=data["class_id"])
        if request.user != classroom.teacher or student not in classroom.request.all(
        ):
            return error_404(request)
        if data["type"] == "accept":
            classroom.student.add(student)
        classroom.request.remove(student)
        return JsonResponse({}, status=201)
    return error_404(request)


# show error page
def error_404(request):
    return render(request, "Mclass/404.html")


# sending the available options to the filter on the frontend
@csrf_exempt
def show_filter(request):
    if request.method == "POST":
        return JsonResponse({"options": get_options()}, status=201)
    return error_404(request)


@login_required
def add_content(request, id):
    # Get the classroom object by id
    classroom = Classroom.objects.get(id=id)

    if request.method == 'POST':
        if request.user.is_teacher:
            # Get the form data from the request
            name = request.POST.get('cn')
            type = request.POST.get('ct')
            url = request.POST.get('cu')

            # Create a new content object with the form data and the classroom
            content = Content(name=name, type=type, url=url, classroom=classroom)
            # Save the content object to the database
            print(request.POST)
            content.save()

            # Redirect the user to the index view
            return redirect('index')

    # If the request method is not POST return 404
    else:
        return error_404(request)


# the contents lister
@login_required
def show_content(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        class_id = data["class_id"]
        page = data["page"]

        content = Content.objects.all()

        # make a list of dictionaries of classes
        content_list = [c.serialize() for c in content]

        # sort depending on ids
        sorted_content = sorted(content_list,
            key=lambda _: _['id'],
            reverse=True)

        # make a paginator
        pg = Paginator(sorted_content, 10)
        try:
            p = pg.page(page)
        except EmptyPage:
            return error_404(request)

        #return a json response
        return JsonResponse(
            {
                "has_next": p.has_next(),
                "has_previous": p.has_previous(),
                "num_pages": pg.num_pages,
                "content": p.object_list,
            },
            status=201)
    return error_404(request)