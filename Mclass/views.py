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
    if request.method == "POST":
        data = json.loads(request.body)
        filter = data["filter"]
        page = data["page"]
        classes = None
    
        if filter == "all":
            classes = Classroom.objects.all()
        else:
            if request.user.teacher:
                classes = request.user.tclass.all()
            else:
                classes = request.user.sclass.all()
        
        classes_list = [c.serialize() for c in classes]
        sorted_classes = sorted(classes_list, key=lambda _: _['id'], reverse=True)
        
        pg = Paginator(sorted_classes, 10)
        try:
            p = pg.page(page)
        except EmptyPage:
            error_404(request)
            
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

    options = ["Chemistry", "Biology", "Physics", "Computer Science", "Art", "History", "Literature", "Languages", "Music", "Geography", "Other"]
    
    return render(request, "Mclass/create.html", {
        "options": options
    })


# show the user joined classes
def myclasses_view(request):
    pass


def error_404(request):
    return render(request, "Mclass/404.html")