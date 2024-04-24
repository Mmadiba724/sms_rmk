from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Course, Student, EnrolledStudent, Transactions

#
# Create your views here.
def homePage(request):
    list_courses = Course.objects.all()
    list_students = Student.objects.all()
    count_students = len(list_students)
    contxt = {
        'list_courses': list_courses,
        'list_students': list_students,
        'total_students': count_students
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(contxt))


def studentsList(request):
    template = loader.get_template('student_list.html')
    return HttpResponse(template.render())

def courseList(request):
    template = loader.get_template('list_courses.html')
    return HttpResponse(template.render())

def transactions(request):
    template = loader.get_template('transactions.html')
    return HttpResponse(template.render())