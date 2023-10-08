import json
from .utils import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Classroom

# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        error_404(request)
    if request.method == "POST":
        full_name = request.POST["full-name"]
        email = request.POST["email"]
        role = request.POST["role"]
        is_teacher = True if role == "teacher" else False

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm-password"]
        if password != confirmation:
            return render(request, "Mclass/register.html", {
                "message": "Passwords must match."
            })

        # make sure that fields are not left empty
        if not password or not confirmation or not email or not full_name :
            return render(request, "Mclass/register.html", {
                "message": "All Fields Are Required."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email.lower(), password=password, full_name=full_name, is_teacher=is_teacher)
            user.save()
        except IntegrityError:
            return render(request, "Mclass/register.html", {
                "message": "Email Already Has an Account"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Mclass/register.html")


def login_view(request):
    if request.user.is_authenticated:
        error_404(request)
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
            return render(request, "Mclass/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "Mclass/login.html")


# logout the user
def logout_view(request):
    if not request.user.is_authenticated:
        error_404(request)
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
                kargs["closed"] = True if data["availability"] == "closed" else False
            
            classes = Classroom.objects.filter(**kargs)

        # show classes that contain the search keyword in their title or the details or teacher name
        elif filter == "search":
            sw = data["search_word"]
            classes = Classroom.objects.filter(title__contains=sw) | (Classroom.objects.filter(details__contains=sw)) | (Classroom.objects.filter(teacher__full_name__contains=sw))

        else:
            error_404()

        # make a list of dictionaries of classes
        classes_list = [c.serialize() for c in classes]

        # sort depending on ids
        sorted_classes = sorted(classes_list, key=lambda _: _['id'], reverse=True)

        # make a paginator
        pg = Paginator(sorted_classes, 10)
        try:
            p = pg.page(page)
        except EmptyPage:
            error_404(request)

        #return a json response
        return JsonResponse({
            "has_next": p.has_next(),
            "has_previous": p.has_previous(),
            "num_pages": pg.num_pages,
            "classes": p.object_list,
        }, status=201)
    return render(request, 'Mclass/index.html')


# create a new class
def create_view(request):
    user = request.user
    if not user.is_authenticated and not user.is_teacher:
        error_404(request)

    if request.method == "POST":
        data = request.POST
        private = True
        image = data.get('image')
        if data.get('visibility') == "public":
            private = False

        if image != '':
            if not image_is_valid(image):
                return render(request, "Mclass/create.html", {
                "message": "Invalid Image URL"
            })
        else:
            image = "https://img.freepik.com/free-vector/hand-drawn-flat-design-stack-books-illustration_23-2149341898.jpg"
        
        classroom = Classroom(
            title=data.get('title'),
            image=image,
            category=data.get('category'),
            private=private,
            details=data.get('details'),
            teacher=request.user
        )
        classroom.save()
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "Mclass/create.html", {
        "options": get_options()
    })


# the class view
@login_required
def class_view(request, title, class_id):
    class_object = Classroom.objects.get(id=class_id)
    # enroll students to a class
    if request.method == "POST":
        if not request.user.is_teacher:
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
            error_404(request)
    return render(request, "Mclass/class.html", {
        "data": class_object.serialize(),
        "teacher": class_object.teacher
    })


# show error page
def error_404(request):
    return render(request, "Mclass/404.html")


# sending the available options to the filter on the frontend
@csrf_exempt
def show_filter(request):
    if request.method == "POST":
        return JsonResponse({
            "options": get_options()
        }, status=201)
    error_404(request)