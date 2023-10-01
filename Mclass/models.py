from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    is_teacher = models.BooleanField(default=False)
    username = models.EmailField(unique=True)