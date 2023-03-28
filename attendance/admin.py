from django.contrib import admin
from .models import Department, Course, StudentProfile, UserProfile, Programme, Attendance, Teaching, Enrollment

# Register your models here.

admin.site.register(Attendance)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Programme)
admin.site.register(StudentProfile)
admin.site.register(Teaching)
admin.site.register(Enrollment)

