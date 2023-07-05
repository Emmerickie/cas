from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),

    #login
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),

    #register
    path('user-register', views.registerUser, name="register-user"),
    path('student-register', views.registerStudent, name="register-student"),
    path('register_fingerprint', views.registerFingerprint, name="register-fingerprint"),
    path('register_lecturer_fingerprint', views.registerFingerprintLecturer, name="register-lecturer-fingerprint"),

    #student
    path('student',views.student,name='student-page'),



    #attendances
    path('view_course_attendances',views.view_course_attendances,name='view-course-attendances'),
    path('course/<str:course_id>/attendance',views.course_attendance,name='course-attendance'),
    path('course/<str:course_id>/attendance/summary',views.course_attendance_summary,name='course-attendance-summary'),


     

    
    path('logout',views.logoutuser,name='logout'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-avatar',views.update_avatar,name='update-avatar'),
    path('update-password',views.update_password,name='update-password'),
    path('department',views.department,name='department-page'),
    path('manage_department',views.manage_department,name='manage-department-modal'),
    path(r'manage_department/<int:pk>',views.manage_department,name='edit-department-modal'),
    path('save_department',views.save_department,name='save-department'),
    path('delete_department',views.delete_department,name='delete-department'),
    path('courses',views.courses,name='all-courses-page'),
    path('manage_course',views.manage_course,name='manage-course-modal'),
    path(r'manage_course/<int:pk>',views.manage_course,name='edit-course-modal'),
    path('save_course',views.save_course,name='save-course'),
    path('delete_course',views.delete_course,name='delete-course'),

    path('lecturers',views.lecturers,name='lecturers-page'),
    path('manage_lecturer',views.manage_lecturer,name='manage-lecturer-modal'),
    path(r'view_lecturer/<int:pk>',views.view_lecturer,name='view-lecturer-details'),
    path(r'manage_lecturer/<int:pk>',views.manage_lecturer,name='edit-lecturer-modal'),


    path('save_lecturer',views.save_faculty,name='save-lecturer'),
    path('delete_lecturer/<str:pk>',views.delete_lecturer,name='delete-lecturer'),

    path('programmes',views.programmes,name='programmes-page'),
    path('manage_class',views.manage_class,name='manage-class-modal'),
    path(r'manage_class/<int:pk>',views.manage_class,name='edit-class-modal'),
    path(r'manage_class_student/<int:classPK>',views.manage_class_student,name='class-student-modal'),
    path('save_class_student/',views.save_class_student,name='save-class-student'),
    path(r'view_class/<int:pk>',views.view_class,name='class-page'),
    path('save_class',views.save_class,name='save-class'),
    path('delete_class',views.delete_class,name='delete-class'),
    path('delete_class_student',views.delete_class_student,name='delete-class-student'),
    path('manage_student',views.manage_student,name='manage-student-modal'),
    path(r'view_student/<int:pk>',views.view_student,name='view-student-modal'),
    path(r'manage_student/<int:pk>',views.manage_student,name='edit-student-modal'),
    path('save_student',views.save_student,name='save-student'),
    path('delete_student',views.delete_student,name='delete-student'),
    path('attendance_class',views.attendance_class,name='attendance-class'),
    # path(r'attendance/<int:classPK>',views.attendance,name='attendance-page'),
    # path(r'attendance/<int:classPK>/<str:date>',views.attendance,name='attendance-page-date'),
    # path('save_attendance',views.save_attendance,name='save-attendance'),
    # path('enroll_student',views.enroll_student,name='enroll-student'),

    # schedules
    path('view_course_schedule/', views.view_course_schedule, name='view-course-schedule'),
    path('view_course_schedule/<str:course_id>/schedule', views.course_schedule, name='course-schedule'),
    path('view_course_schedule/<str:course_id>/schedule/add_schedule', views.add_schedule, name='add-schedule'),

    
    path('add_schedule/', views.add_schedule, name='add-schedule'),
    path('lecturer/timetable/', views.lecturer_timetable, name='lecturer_timetable'),
    path('lecturer/<str:pk>/courses',views.lecturer_courses,name='lecturer-courses-page'),
    path('lecturer/<str:pk>/add_lecturing_course',views.add_lecturing_course,name='add-lecturing-course'),


    #academic year
    
    path('academic_year/new/', views.new_academic_year, name='new-academic-year'),
    path('course/<str:course_id>/', views.course_details, name='course-details'),
    path('course/<str:course_id>/enroll_students',views.enroll_students_in_course,name='enroll-students'),
    

    # path("add-teaching/", views.add_teaching, name="add-teaching"),

    #attendance
    path('student_attendance',views.student_attendance,name='student-attendance'),



]
