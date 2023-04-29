from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegistration, UserChangeForm

from .models import Department, Course, StudentProfile, UserProfile, Programme, Attendance, Teaching, Enrollment, User

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

