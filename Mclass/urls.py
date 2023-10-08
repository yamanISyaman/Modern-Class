from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('create', views.create_view, name="create"),
    path('filter', views.show_filter, name="filter"),
    path('class/students', views.students_view, name="students"),
    path('class/kick', views.kick_student, name="kick"),
    path('class/<str:title>+<int:class_id>', views.class_view, name="class_view"),
]
