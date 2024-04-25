from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Course, Student, EnrolledStudent, Transactions


#
# Create your views here.
def homePage(request):
    # Statistics
    count_students = Student.objects.count()
    count_courses = Course.objects.count()
    count_enrolled_students = EnrolledStudent.objects.count()
    count_transactions = Transactions.objects.count()
    recent_students = Student.objects.all()[:10]
    courses = Course.objects.all()
    context = {
        "count_students": count_students,
        "count_courses": count_courses,
        "count_enrolled_students": count_enrolled_students,
        "count_transactions": count_transactions,
        "courses": courses,
        "recent_students": recent_students,
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context))


def studentsList(request):
    template = loader.get_template("student_list.html")
    return HttpResponse(template.render())


def addStudent(request):
    message = None
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        student_obj = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=age,
            gender=gender,
        )
        student_obj.save()
        message = "Student added successfully"
    
    all_courses = Course.objects.all()
    context = {"message": message, 'all_courses': all_courses}
    template = loader.get_template("add_student.html")
    return HttpResponse(template.render(context))


def viewStudent(request, student_id):
    student_obj = Student.objects.get(id=student_id)
    all_transactions = Transactions.objects.filter(student_id=student_id)
    enrollments = EnrolledStudent.objects.filter(student_id=student_id)
    context = {
        "student": student_obj,
        "all_transactions": all_transactions,
        "enrollments": enrollments,
    }
    template = loader.get_template("view_student.html")
    return HttpResponse(template.render(context))


def courseList(request):
    template = loader.get_template("list_courses.html")
    return HttpResponse(template.render())


def transactions(request):
    template = loader.get_template("transactions.html")
    return HttpResponse(template.render())
