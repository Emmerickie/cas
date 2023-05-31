from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegistration, UserChangeForm

from .models import Department, Course, StudentProfile, UserProfile, Programme, Attendance, Teaching, Enrollment, User, Venue, Schedule, AcademicTerm, Semester, StudentAttendance, InstructorAttendance, ProgrammeCourse

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    form = UserRegistration
    add_form = UserChangeForm
    list_display = ('email', 'first_name', 'is_admin', 'is_staff')

admin.site.register(Attendance)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Programme)
admin.site.register(StudentProfile)
admin.site.register(Teaching)
admin.site.register(Enrollment)
admin.site.register(User)
admin.site.register(Venue)
admin.site.register(Schedule)
admin.site.register(AcademicTerm)
admin.site.register(Semester)
admin.site.register(StudentAttendance)
admin.site.register(InstructorAttendance)
admin.site.register(ProgrammeCourse)
