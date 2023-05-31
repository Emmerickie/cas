from unicodedata import category
from aiohttp import request
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json
import pytz
from datetime import datetime, timedelta
from datetime import date
# from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from ams.settings import MEDIA_ROOT, MEDIA_URL
from django.core.exceptions import ValidationError

from attendance.models import *
from attendance.forms import UserRegistration, StudentRegistration, UpdateProfile, UpdateProfileMeta, UpdateProfileAvatar, AddAvatar, SaveDepartment, SaveCourse, SaveProgramme, SaveStudent, SaveClassStudent, UpdatePasswords, UpdateFaculty, StudentProfileForm, EnrollForm, AcademicYearForm, Semester1Form, Semester2Form

deparment_list = Department.objects.exclude(status = 2).all()
context = {
    'page_title' : 'Simple Blog Site',
    'deparment_list' : deparment_list,
    'deparment_list_limited' : deparment_list[:3]
}
#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    context['page_title'] = 'Home'
    departments = Department.objects.count()
    Programmes = Programme.objects.count()
    courses = Course.objects.count()
    faculty = UserProfile.objects.filter(user_type = 2).count()
    if request.user.profile.user_type == 1:
        students = StudentProfile.objects.count()
        courses = Course.objects.count()
    elif request.user.profile.user_type == 2:
        courses = Teaching.objects.filter(lecturer = request.user.profile).count()
        students = Enrollment.objects.filter(course__in = Teaching.objects.filter(lecturer = request.user.profile).values_list('id')).count()
    
    else:
        courses = Enrollment.objects.filter(student = request.user.student).count()
    context['departments'] = departments
    context['courses'] = courses
    context['faculty'] = faculty
    context['students'] = students
    context['programme'] = Programmes



    # context['posts'] = posts
    return render(request, 'home.html',context)



def registerUser(request):
    department = Department.objects.filter(status=1).all()

    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register Instructor"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            User.is_staff=True
            user = form.save(commit=False)
            user.set_password((form.cleaned_data['last_name']).upper())
            user.save()
            
            newUser = User.objects.all().last()
            try:
                profile = UserProfile.objects.get(user = newUser)
            except:
                profile = None

            UserProfile.objects.create(user=user, gender=user.gender, department=user.department)

            # if profile is None:
            #     if User.is_admin:
            #         UserProfile(user = newUser, contact= data['contact'], avatar = request.FILES['avatar'], user_type=1).save()
                
            #     else:
            #         UserProfile(user = newUser, contact= data['contact']).save()
            # else:
            #     UserProfile.objects.filter(id = profile.id).update(user = newUser, contact= data['contact'])
            #     avatar = AddAvatar(request.POST,request.FILES, instance = profile)
            #     if avatar.is_valid():
            #         avatar.save()
            
            return redirect('home-page')
    else:
        form = UserRegistration()
        context['reg_form'] = form

    return render(request,'register.html',context)

def registerStudent(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('home-page')
    context = {}
    context['page_title'] = "Register Student"
    if request.POST:
        user_form = StudentRegistration(request.POST)
        student_form = StudentProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password((user_form.cleaned_data['last_name']).upper())
            user.save()

            StudentProfile.objects.create(user=user, programme=user.programme, student_id=user, year_of_study=user.year_of_study)
            # student_profile = student_form.save(commit=False)
            # student_profile.user = user
            # student_profile.student_id = user_form.cleaned_data['username']
            # student_profile.first_name = user_form.cleaned_data['first_name']
            # student_profile.middle_name = user_form.cleaned_data['middle_name']
            # student_profile.last_name = user_form.cleaned_data['last_name']
                    
            # student_profile.save()


            # newStudent = User.objects.all().last()


            
            # try:
            #     profile = StudentProfile.objects.get(user = newStudent)
            # except:
            #     profile = None
            # if profile is None:
            #     StudentProfile(user = newStudent, dob= data['dob'], contact= data['contact'], address= data['address'], avatar = request.FILES['avatar']).save()
            # else:
            #     StudentProfile.objects.filter(id = profile.id).update(user = newStudent, dob= data['dob'], contact= data['contact'], address= data['address'])
            #     avatar = AddAvatar(request.POST,request.FILES, instance = profile)
            #     if avatar.is_valid():
            #         avatar.save()

            return redirect('home-page')
    else:
        user_form = StudentRegistration()
        student_form = StudentProfileForm()
    context['register_student_form'] = user_form
    context['student_profile_form'] = student_form

    return render(request,'register_student.html', context)



@login_required
def profile(request):
    context = {
        'page_title':"My Profile"
    }

    return render(request,'profile.html',context)
    
@login_required
def update_profile(request):
    context['page_title'] = "Update Profile"
    user = User.objects.get(id= request.user.id)
    profile = UserProfile.objects.get(user= user)
    context['userData'] = user
    context['userProfile'] = profile
    if request.method == 'POST':
        data = request.POST
        # if data['password1'] == '':
        # data['password1'] = '123'
        form = UpdateProfile(data, instance=user)
        if form.is_valid():
            form.save()
            form2 = UpdateProfileMeta(data, instance=profile)
            if form2.is_valid():
                form2.save()
                messages.success(request,"Your Profile has been updated successfully")
                return redirect("profile")
            else:
                # form = UpdateProfile(instance=user)
                context['form2'] = form2
        else:
            context['form1'] = form
            form = UpdateProfile(instance=request.user)
    return render(request,'update_profile.html',context)


@login_required
def update_avatar(request):
    context['page_title'] = "Update Avatar"
    user = User.objects.get(id= request.user.id)
    context['userData'] = user
    context['userProfile'] = user.profile
    if user.profile.avatar:
        img = user.profile.avatar.url
    else:
        img = MEDIA_URL+"/default/default-avatar.png"

    context['img'] = img
    if request.method == 'POST':
        form = UpdateProfileAvatar(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Profile has been updated successfully")
            return redirect("profile")
        else:
            context['form'] = form
            form = UpdateProfileAvatar(instance=user)
    return render(request,'update_avatar.html',context)

@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

#Department
@login_required
def department(request):
    departments = Department.objects.all()
    context['page_title'] = "Department Management"
    context['departments'] = departments
    return render(request, 'department_mgt.html',context)

@login_required
def manage_department(request,pk=None):
    # department = department.objects.all()
    if pk == None:
        department = {}
    elif pk > 0:
        department = Department.objects.filter(id=pk).first()
    else:
        department = {}
    context['page_title'] = "Manage Department"
    context['department'] = department

    return render(request, 'manage_department.html',context)

@login_required
def save_department(request):
    resp = { 'status':'failed' , 'msg' : '' }
    context = {}
    if request.POST:
        form = SaveDepartment(request.POST)
        if form.is_valid:
            form.save()
            return redirect('department-page')
            
    else:
        form = SaveDepartment()
        context['Save_department_form'] = form

    return render(request, 'manage_department.html', context)

@login_required
def delete_department(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            department = Department.objects.filter(id = id).first()
            department.delete()
            resp['status'] = 'success'
            messages.success(request,'Department has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")


#Course
@login_required
def course(request):
    courses = Course.objects.all()
    context['page_title'] = "Course Management"
    context['courses'] = courses
    return render(request, 'course_mgt.html',context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    current_semester = Semester.objects.filter(start_date__lte=date.today(), end_date__gte=date.today()).first()
    lecturers = Teaching.objects.filter(course=course)
    programmes = ProgrammeCourse.objects.filter(course=course)
    students = Enrollment.objects.filter(course=course, semester=current_semester)
    context = { 
        'course': course,
        'current_semester': current_semester,
        'programmes': programmes,
        'lecturers': lecturers,
        'students':students
    }
    
    return render(request, 'course_details.html', context)

@login_required
def manage_course(request,pk=None):
    # course = course.objects.all()
    if pk == None:
        course = {}
        department = Department.objects.filter(status=1).all()
    elif pk > 0:
        course = Course.objects.filter(id=pk).first()
        department = Department.objects.filter(Q(status=1) or Q(id = course.id)).all()
    else:
        department = Department.objects.filter(status=1).all()
        course = {}
    context['page_title'] = "Manage Course"
    context['departments'] = department
    context['course'] = course

    return render(request, 'manage_course.html',context)

@login_required
def save_course(request):
    resp = { 'status':'failed' , 'msg' : '' }
    context = {}
    if request.POST:
        form = SaveCourse(request.POST)
        if form.is_valid:
            form.save()
            return redirect('course-page')
            
    else:
        form = SaveCourse()
        context['Save_course_form'] = form

    return render(request, 'manage_course.html', context)

@login_required
def delete_course(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            course = Course.objects.filter(id = id).first()
            course.delete()
            resp['status'] = 'success'
            messages.success(request,'Course has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")

#Faculty
@login_required
def faculty(request):
    user = UserProfile.objects.filter(user_type = 2).all()
    context['page_title'] = "Faculty Management"
    context['faculties'] = user
    return render(request, 'faculty_mgt.html',context)

@login_required
def manage_faculty(request,pk=None):
    if pk == None:
        faculty = {}
        department = Department.objects.filter(status=1).all()
    elif pk > 0:
        faculty = UserProfile.objects.filter(id=pk).first()
        department = Department.objects.filter(Q(status=1) or Q(id = faculty.id)).all()
    else:
        department = Department.objects.filter(status=1).all()
        faculty = {}
    context['page_title'] = "Manage Faculty"
    context['departments'] = department
    context['faculty'] = faculty
    return render(request, 'manage_faculty.html',context)

@login_required
def view_faculty(request,pk=None):
    if pk == None:
        faculty = {}
    elif pk > 0:
        faculty = UserProfile.objects.filter(id=pk).first()
    else:
        faculty = {}
    context['page_title'] = "Manage Faculty"
    context['faculty'] = faculty
    return render(request, 'faculty_details.html',context)

@login_required
def save_faculty(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if request.method == 'POST':
        data = request.POST
        if data['id'].isnumeric() and data['id'] != '':
            user = User.objects.get(id = data['id'])
        else:
            user = None
        if not user == None:
            form = UpdateFaculty(data = data, user = user, instance = user)
        else:
            form = UserRegistration(data)
        if form.is_valid():
            form.save()

            if user == None:
                user = User.objects.all().last()
            try:
                profile = UserProfile.objects.get(user = user)
            except:
                profile = None
            if profile is None:
                form2 = UpdateProfileMeta(request.POST,request.FILES)
            else:
                form2 = UpdateProfileMeta(request.POST,request.FILES, instance = profile)
                if form2.is_valid():
                    form2.save()
                    resp['status'] = 'success'
                    messages.success(request,'Faculty has been save successfully.')
                else:
                    User.objects.filter(id=user.id).delete()
                    for field in form2:
                        for error in field.errors:
                            resp['msg'] += str(error + '<br>')
            
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error + '<br>')

    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def delete_faculty(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            faculty = User.objects.filter(id = id).first()
            faculty.delete()
            resp['status'] = 'success'
            messages.success(request,'Faculty has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")


    
#Class
@login_required
def classPage(request):
    if request.user.profile.user_type == 1:
        programmes = Programme.objects.all()
    else:
        programmes = Programme.objects.filter(assigned_faculty = request.user.profile).all()

    context['page_title'] = "Programme Management"
    context['programmes'] = programmes
    return render(request, 'class_mgt.html',context)

@login_required
def manage_class(request,pk=None):
    departments =Department.objects.all()
    if pk == None:
        programme = {}
    elif pk > 0:
        programme = Programme.objects.filter(id=pk).first()
    else:
        programme = {}
    context['page_title'] = "Manage Programme"
    context['departments'] = departments
    context['programme'] = programme

    return render(request, 'manage_class.html',context)

@login_required
def view_class(request, pk= None):
    if pk is None:
        return redirect('home-page')
    else:
        programme = Programme.objects.filter(id=pk).first()
        students = StudentProfile.objects.filter(programme = programme).all()
        context['programme'] = programme
        context['students'] = students
        context['page_title'] = "Programme Information"
    return render(request, 'class_details.html',context)


@login_required
def save_class(request):
    resp = { 'status':'failed' , 'msg' : '' }
    context = {}
    if request.POST:
        form = SaveProgramme(request.POST)
        if  form.is_valid:
            form.save()
            return redirect('class-page')
            
    else:
        form = SaveProgramme()
        context['Save_programme_form'] = form

    return render(request, 'manage_class.html', context)

@login_required
def delete_class(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            _class = Class.objects.filter(id = id).first()
            _class.delete()
            resp['status'] = 'success'
            messages.success(request,'Class has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")

def new_academic_year(request):
    context['page_title'] = "New Academic Year"
    if request.POST:
        form = AcademicYearForm(request.POST)
        form1 = Semester1Form(request.POST)
        form2 = Semester2Form(request.POST)
        if  form1.is_valid and form2.is_valid:
            semester_1 = form1.save(commit=False)
            semester_2 = form2.save(commit=False)
            academic_year = form.save(commit=False)

            # Set the academic year for semesters
            semester_1.academic_year = academic_year
            semester_2.academic_year = academic_year

            # Set the semester values
            semester_1.semester = '1'
            semester_2.semester = '2'

            academic_year.start_date = semester_1.start_date
            academic_year.end_date = semester_2.end_date

            # Save the objects
            academic_year.save()
            semester_1.save()
            semester_2.save()

            
            # Update students' year of study and status
            update_students_year_of_study(academic_year)
        return redirect('success')
            
    else:
        form = AcademicYearForm()
        form1 = Semester1Form()
        form2 = Semester2Form()

    context['academic_year_form'] = form
    context['semester1_form'] = form1
    context['semester2_form'] = form2


    return render(request, 'new_academic_year.html', context)



def update_students_year_of_study(self):
    students = StudentProfile.objects.all()
    for student in students:
            last_modified_date = student.date_updated.date()
            current_date = date.today()
            year_diff = (current_date - last_modified_date).days // 365  # Get the difference in years

            new_year_of_study = int(student.year_of_study) + year_diff

            # Check if the new year of study exceeds the program duration
            if new_year_of_study > int(student.programme.duration):
                student.status = 'completed'
            else:
                student.year_of_study = str(new_year_of_study)

            student.save()


def enroll_student(request):
    context = {}
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
            if created:
                # If a new enrollment was created
                return redirect('enrollment_success')
            else:
                # If the enrollment already exists
                form.add_error(None, 'This student is already enrolled in this course.')
    else:
        form = EnrollForm()
        context['enroll_form'] = form
    return render(request, 'enroll_student.html', context)

def enroll_students_in_course(request, course_id):


    current_semester = Semester.objects.filter(start_date__lte=date.today(), end_date__gte=date.today()).first()
    course = get_object_or_404(Course, course_id=course_id)

    # if course.semester != current_semester.semester:
    #     return

    # eligible_programmes =  ProgrammeCourse.objects.filter(course=course)

    # eligible_students = StudentProfile.objects.filter(
    #     programme=course,
    #     year_of_study=course.programmecourse.level,
    #     status='continuing'
    # )

    # eligible_students = eligible_students.filter(
    #     # enrollment__isnull=True,
    #     course__programmecourse__course=course,
    #     course__programmecourse__course_type='C',
    #     course__semester=current_semester.semester
    # ).distinct()


    eligible_programmes = ProgrammeCourse.objects.filter(course=course, semester=current_semester.semester, status='C')
    if eligible_programmes.exists():
        for eligible_programme in eligible_programmes:
            level = eligible_programme.level
            # Enroll students who have the course as a core, matching level, status as Continuing, and program status as Core
            students = StudentProfile.objects.filter(programme=eligible_programme.programme, year_of_study=level, status='Continuing')
            
            for student in students:
                # Enroll the student in the course for the current semester
                Enrollment.objects.create(student=student, course=course, semester=current_semester)

                # initialize the attendance which may we should put it to when schedule is created or modified
            current_semester = Semester.objects.filter(start_date__lte=date.today(), end_date__gte=date.today()).first()
            course = get_object_or_404(Course, course_id=course_id)


            schedule_lessons = Schedule.objects.filter(course=course)

            if schedule_lessons.exists():
                for schedule_lesson in schedule_lessons:
                    start_date = current_semester.start_date
                    end_date = current_semester.end_date

                    if start_date <= end_date:
                        current_date = start_date
                        while current_date <= end_date:
                            if current_date.strftime('%A') == schedule_lesson.day:
                                attendance = Attendance.objects.create(date=current_date, lesson=schedule_lesson)

                                eligible_students = Enrollment.objects.filter(course=course, semester=current_semester).values_list('student_id', flat=True)
                                for student_id in eligible_students:
                                    StudentAttendance.objects.create(attendance=attendance, student_id=student_id)

                            current_date += timedelta(days=1)
                # create response or redirect

            else:
                raise ValidationError("No schedule found for the course.")

                
    else:
        raise ValidationError("Invalid semester or course.")
    







@login_required
def manage_class_student(request,classPK = None):
    if classPK is None:
        return HttpResponse('Class ID is Unknown')
    else:
        context['classPK'] = classPK
        _class  = Class.objects.get(id = classPK)
        # print(ClassStudent.objects.filter(classIns = _class))
        students = Student.objects.exclude(id__in = ClassStudent.objects.filter(classIns = _class).values_list('student').distinct()).all()
        context['students'] = students
        return render(request, 'manage_class_student.html',context)
    

@login_required
def save_class_student(request):
    resp = {'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        form = SaveClassStudent(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Student has been added successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error+"<br>")
    return HttpResponse(json.dumps(resp),content_type = 'json')

@login_required
def delete_class_student(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            cs = ClassStudent.objects.filter(id = id).first()
            cs.delete()
            resp['status'] = 'success'
            messages.success(request,'Student has been deleted from Class successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")


#Student
@login_required
def student(request):
    students = StudentProfile.objects.all()
    context['page_title'] = "Student Management"
    context['students'] = students
    return render(request, 'student_mgt.html',context)

@login_required
def manage_student(request,pk=None):
    # course = course.objects.all()
    if pk == None:
        student = {}
        programmes = Programme.objects.all()
    elif pk > 0:
        student = StudentProfile.objects.filter(id=pk).first()

        programme = student.programme
    else:
        programmes = Programme.objects.all()
        student = {}
    context['page_title'] = "Manage Student"
    context['programmes'] = programmes
    context['student'] = student

    return render(request, 'manage_student.html',context)

@login_required
def view_student(request,pk=None):
    if pk == None:
        student = {}
    elif pk > 0:
        student = StudentProfile.objects.filter(id=pk).first()
    else:
        student = {}
    context['student'] = student
    return render(request, 'student_details.html',context)

@login_required
def save_student(request):
    resp = { 'status':'failed' , 'msg' : '' }
    context = {}
    if request.POST:
        form = SaveStudent(request.POST)
        if  form.is_valid:
            form.save()
            return redirect('student-page')
            
    else:
        form = SaveStudent()
        context['Save_student_form'] = form

    return render(request, 'manage_student.html', context)

@login_required
def delete_student(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            student = Student.objects.filter(id = id).first()
            student.delete()
            resp['status'] = 'success'
            messages.success(request,'Student Details has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")


def lecturer_timetable(request):
    # Assuming you have the logged-in lecturer user object
    lecturer = request.user.profile

    # Get the courses taught by the lecturer
    courses_taught = Teaching.objects.filter(lecturer=lecturer).values_list('course', flat=True)

    # Get the schedules for the courses taught by the lecturer
    schedules = Schedule.objects.filter(course__in=courses_taught)

    context = {
        'schedules': schedules,
    }

    return render(request, 'lecturer_timetable.html', context)

#Attendance
@login_required
def attendance_class(request):
    if request.user.profile.user_type == 1:
        classes = Class.objects.all()
    else:
        classes = Class.objects.filter(assigned_faculty = request.user.profile).all()
    context['page_title'] = "Attendance Management"
    context['classes'] = classes
    return render(request, 'attendance_class.html',context)


@login_required
def student_attendance(request):
    # Get the current date and time
    # Implement your fingerprint recognition logic to retrieve the user's fingerprint data

    # Find the current course based on the schedule
    current_course = Schedule.objects.filter(start_time__lte=current_time, end_time__gte=current_time).first()

    # Check if the student is enrolled in the current course
    enrolled = Enrollment.objects.filter(student=request.user.student, course=current_course.course).exists()

    # Check if the course is an elective for the student's programme
    elective = ProgrammeCourse.objects.filter(programme=request.user.student.programme, level = request.user.student.year_of_study, course=current_course.course, course_type='E').exists()

    if not enrolled and elective:
        # Add the student to enrollment
        Enrollment.objects.create(student=request.user.student, course=current_course.course)

    # Record the student's attendance  ?  ,created
    attendance = Attendance.objects.get_or_create(lesson=current_course, date=current_date)
    StudentAttendance.objects.create(lesson=attendance, student=request.user.student, time=current_time)

    return HttpResponse("Attendance recorded successfully!")

@login_required
def lecturer_attendance(request):
    # Get the current date and time
    # Implement your fingerprint recognition logic to retrieve the user's fingerprint data

    # Find the current course based on the schedule
    current_course = Schedule.objects.filter(start_time__lte=current_time, end_time__gte=current_time).first()

    # Check if the lecturer is assigned to teach the current course
    assigned = Teaching.objects.filter(lecturer=request.user.lecturer, course=current_course.course).exists()

    if assigned:
        attendance, created = Attendance.objects.get_or_create(lesson=current_course, date=current_date)

        # Record the lecturer's attendance

        InstructorAttendance.objects.create(lecturer=request.user.lecturer, lesson=attendance, time=current_time)

    return HttpResponse("Attendance recorded successfully!")


def course_attendance(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    schedules = Schedule.objects.filter(course=course)



    if len(schedules) == 0:
        # No schedules found for the course
        return render(request, 'no_schedule.html', {'course': course})
    
    current_date = timezone.now().date()
    students = StudentProfile.objects.filter(enrollment__course=course).distinct()
    attendances = Attendance.objects.filter(lesson__in=schedules, date__lte=current_date)

    # Fetch student attendances for the given course and attendance dates
    student_attendances = StudentAttendance.objects.filter(
        attendance__in=attendances,
        student__in=students
    )

    # Create a dictionary to store student attendances indexed by student and attendance date
    attendance_dict = {}
    for student_attendance in student_attendances:
        attendance_dict.setdefault(student_attendance.student, {})[student_attendance.attendance] = student_attendance.is_present

    context = {
        'course': course,
        'students': students,
        'attendances': attendances,
        'attendance_dict': attendance_dict
    }

    return render(request, 'course_attendance.html', context)

    # Retrieve the current date and time from today above
    # current_time = today.time()
    # current_date = today.date()


    # context = {
    #     'course': course,
    #     'schedules': current_schedules,
    #     'student_attendances': student_attendances,
    #     # 'student_attendance': student_attendance,
    # }

    

    # # Check if the current date and time fall within any of the scheduled lessons
    # current_schedules = []
    # for schedule in schedules:

    #     if schedule.day == today.strftime('%A') and schedule.start_time <= current_time <= schedule.end_time:
    #         current_schedules.append(schedule)
    #         attendance, created = Attendance.objects.get_or_create(lesson=schedule, date=current_date )



            
                

    # enrollments = Enrollment.objects.filter(course=course)

    # for enrollment in enrollments:
    #         student = enrollment.student
    #         student_attendance, created = StudentAttendance.objects.get_or_create(attendance=attendance, student=student)

    
    
    # student_attendances = StudentAttendance.objects.filter(attendance=attendance)

    
    # else:
    #     # Current date and time do not fall within any of the scheduled lessons
    #     previous_attendances = Attendance.objects.filter(lesson__course=course)

    #     context = {
    #         'course': course,
    #         'previous_attendances': previous_attendances,
    #     }

    #     return render(request, 'previous_attendance.html', context)

# def course_attendance(request, course_id, classPK = None, date=None):
#     course = get_object_or_404(Course, course_id=course_id)



#     _class = Class.objects.get(id = classPK)
#     students = Student.objects.filter(id__in = ClassStudent.objects.filter(classIns = _class).values_list('student')).all()
#     context['page_title'] = "Attendance Management"
#     context['class'] = _class
#     context['date'] = date
#     att_data = {}
#     for student in students:
#         att_data[student.id] = {}
#         att_data[student.id]['data'] = student
#     if not date is None:
#         date = datetime.strptime(date, '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#         attendance = Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day, classIns = _class).all()
#         for att in attendance:
#             att_data[att.student.pk]['type'] = att.type
#     print(list(att_data.values()))
#     context['att_data'] = list(att_data.values())
#     context['students'] = students

#     return render(request, 'attendance_mgt.html',context)

# @login_required
# def save_attendance(request):
#     resp = {'status' : 'failed', 'msg':''}
#     if request.method == 'POST':
#         post = request.POST
#         date = datetime.strptime(post['attendance_date'], '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#         _class = Class.objects.get(id=post['classIns'])
#         Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day,classIns = _class).delete()
#         for student in post.getlist('student[]'):
#             type = post['type['+student+']']
#             studInstance = Student.objects.get(id = student)
#             att = Attendance(student=studInstance,type = type,classIns = _class,attendance_date=post['attendance_date']).save()
#         resp['status'] = 'success'
#         messages.success(request,"Attendance has been saved successfully.")
#     return HttpResponse(json.dumps(resp),content_type="application/json")