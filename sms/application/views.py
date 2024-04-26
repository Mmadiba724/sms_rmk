from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Course, Student, EnrolledStudent, Transactions
import datetime
from django.db.models import Sum, Avg


# Create your views here.
def homePage(request):
    # Statistics
    count_students = Student.objects.count()
    count_courses = Course.objects.count()
    count_enrolled_students = EnrolledStudent.objects.count()
    count_transactions = Transactions.objects.count()
    recent_students = Student.objects.all().order_by('-id')
    courses = Course.objects.all()
    context = {
        "count_students": count_students,
        "count_courses": count_courses,
        "count_enrolled_students": count_enrolled_students,
        "count_transactions": count_transactions,
        "courses": courses,
        "recent_students": recent_students
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context))


def studentsList(request):
    if request.method == "POST":
        query = request.POST['query']
        all_students = Student.objects.filter(first_name__contains=query)
    else:
        all_students = Student.objects.all()
    result_count = len(all_students)
    context = {
        'all_students': all_students,
        'result_count': result_count
    }
    template = loader.get_template("student_list.html")
    return HttpResponse(template.render(context))


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
    context = {"message": message}
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
    all_course_list = Course.objects.all()
    result_count = len(all_course_list)
    context = {
        "all_course_list": all_course_list,
        "result_count": result_count,
    }
    template = loader.get_template("list_courses.html")
    return HttpResponse(template.render(context))

def addCourse(request):
    message = None
    if request.method == "POST":
        course_name = request.POST["course_name"]
        course_desc = request.POST["course_desc"]
        course_duration = request.POST["duration"]
        course_price = request.POST["price"]
        start_date = request.POST["date"]
        course_obj = Course.objects.create(
            course_name=course_name,
            course_desc=course_desc,
            course_duration=course_duration,
            course_price=course_price,
            start_date=start_date,
        )
        course_obj.save()
        message = "Course added successfully"
    context = {"message": message}
    template = loader.get_template("add_course.html")
    return HttpResponse(template.render(context))


def viewCourse(request, course_id):
    course_obj = Course.objects.get(id=course_id)
    students_enrolled = EnrolledStudent.objects.filter(course_id=course_id).count()
    start_date = course_obj.start_date
    time_delta = datetime.timedelta(days=course_obj.course_duration*7)
    end_date = start_date + time_delta
    context = {
        "course_obj": course_obj,
        "students_enrolled": students_enrolled,
        "end_date": end_date
    }
    template = loader.get_template("view_course.html")
    return HttpResponse(template.render(context))

def transactions(request):
    all_transactions = Transactions.objects.all().order_by('-id')
    # Total Amount recieve, Total amount today, Total Transactions, Average amount per transaction
    total_transactions = Transactions.objects.count()
    total_agg = Transactions.objects.aggregate(total=Sum('amount')) # = {'total': 180 }
    total_amount = total_agg['total']
    total_agg_today = Transactions.objects.filter(date__gte='2024-04-26').aggregate(today_today=Sum('amount'))
    total_today = total_agg_today['today_today']
    average_agg = Transactions.objects.aggregate(total_average=Avg('amount'))
    total_avg = average_agg['total_average']
    context = {
        "all_transactions": all_transactions,
        "total_transactions": total_transactions,
        "total_amount": total_amount,
        "total_today": total_today,
        "total_avg": total_avg,
    }
    template = loader.get_template("transactions.html")
    return HttpResponse(template.render(context))
