from unicodedata import category
from aiohttp import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
# from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from ams.settings import MEDIA_ROOT, MEDIA_URL
from attendance.models import Attendance, UserProfile,Course, Department, StudentProfile, Course, Enrollment, Teaching, Programme, User

from attendance.forms import UserRegistration, StudentRegistration, UpdateProfile, UpdateProfileMeta, UpdateProfileAvatar, AddAvatar, SaveDepartment, SaveCourse, SaveProgramme, SaveStudent, SaveClassStudent, UpdatePasswords, UpdateFaculty, StudentProfileForm

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

            StudentProfile.objects.create(user=user, programme=user.programme, student_id=user)
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
            return render(request, 'department_mgt.html')
            
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
def attendance(request,classPK = None, date=None):
    _class = Class.objects.get(id = classPK)
    students = Student.objects.filter(id__in = ClassStudent.objects.filter(classIns = _class).values_list('student')).all()
    context['page_title'] = "Attendance Management"
    context['class'] = _class
    context['date'] = date
    att_data = {}
    for student in students:
        att_data[student.id] = {}
        att_data[student.id]['data'] = student
    if not date is None:
        date = datetime.strptime(date, '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        attendance = Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day, classIns = _class).all()
        for att in attendance:
            att_data[att.student.pk]['type'] = att.type
    print(list(att_data.values()))
    context['att_data'] = list(att_data.values())
    context['students'] = students

    return render(request, 'attendance_mgt.html',context)

@login_required
def save_attendance(request):
    resp = {'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        post = request.POST
        date = datetime.strptime(post['attendance_date'], '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        _class = Class.objects.get(id=post['classIns'])
        Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day,classIns = _class).delete()
        for student in post.getlist('student[]'):
            type = post['type['+student+']']
            studInstance = Student.objects.get(id = student)
            att = Attendance(student=studInstance,type = type,classIns = _class,attendance_date=post['attendance_date']).save()
        resp['status'] = 'success'
        messages.success(request,"Attendance has been saved successfully.")
    return HttpResponse(json.dumps(resp),content_type="application/json")