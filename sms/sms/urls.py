"""
URL configuration for sms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application.views import homePage, studentsList, courseList, transactions, addStudent, viewStudent


urlpatterns = [
    path('', homePage, name="home"),
    # Students Paths
    path('students/', studentsList, name="students"),
    path('student/add/', addStudent, name="addStudent"),
    path('student/view/<int:student_id>', viewStudent, name="viewStudent"),
    # Courses Path
    path('courses/', courseList, name="courses"),
    path('transactions/', transactions, name="transactions"),
]
