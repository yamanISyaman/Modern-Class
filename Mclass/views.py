import json
from .utils import image_is_valid
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
    return render(request, 'Mclass/index.html')


# create a new class
def create_view(request):
    user = request.user
    if not user.is_authenticated and not user.is_teacher:
        error_404(request)

    options = ["Chemistry", "Biology", "Physics", "Computer Science", "Art", "History", "Literature", "Languages", "Music", "Geography", "Other"]

    if request.method == "POST":
        data = request.POST
        private = True
        image = data["image"]
        if data['visibility'] == "public":
            private = False

        if image != '':
            if not image_is_valid(image):
                return render(request, "Mclass/create.html", {
                "message": "Invalid Image URL"
            })
        
        classroom = Classroom(
            title=data['title'],
            image=data['image'],
            category=data['category'],
            private=private,
            details=data['details'],
            teacher=request.user
        )
        classroom.save()
        return render(request, "Mclass/index.html")
        
    return render(request, "Mclass/create.html", {
        "options": options
    })


# show the user joined classes
def myclasses_view(request):
    pass


def error_404(request):
    return render(request, "Mclass/404.html")