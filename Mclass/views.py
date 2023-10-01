import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User

# Create your views here.

def register_view(request):
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
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    return render(request, 'Mclass/index.html')