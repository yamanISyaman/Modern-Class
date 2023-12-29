from django.contrib import admin
from .models import Classroom, User, Content

# Register your models here.

admin.site.register(User, admin.ModelAdmin)
admin.site.register(Classroom, admin.ModelAdmin)
admin.site.register(Content, admin.ModelAdmin)
