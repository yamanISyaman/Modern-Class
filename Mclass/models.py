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
    request = models.ManyToManyField(User, related_name="request")

    
    def serialize(self):
        return {
            "id": self.id,
            "teacher": self.teacher.full_name,
            "title": self.title,
            "image": self.image,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "category": self.category,
            "details": self.details,
            "private": self.private,
            "closed": self.closed,
            "students": [s.id for s in self.student.all()],
            "requests": [r.id for r in self.request.all()],
        }