from django.contrib import admin
from .models import Classroom, User

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    pass

class CustomClassroom(admin.ModelAdmin):
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(Classroom, CustomClassroom)