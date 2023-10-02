from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# User Model
class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    is_teacher = models.BooleanField(default=False)


# Class Model
class Classroom(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(blank=True, default='')
    private = models.BooleanField(default=False)
    category = models.CharField(max_length=30)
    closed = models.BooleanField(default=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tclass")
    student = models.ManyToManyField(User, related_name="sclass")