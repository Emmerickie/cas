from multiprocessing.spawn import old_main_modules
from statistics import mode
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
class Department(models.Model):

    STATUS = (
        (1, 'Active'),
        (2, 'Inactive')
    )

    department_id = models.CharField(max_length=100, unique=True)
    name = models.TextField(max_length=250)
    status = models.IntegerField(default = 1, choices=STATUS)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_id

class Programme(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    programme_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=250)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.programme_id

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given     , email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, permissions, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        user = self._create_user(username, email, password, **extra_fields)
        
        # user = self.create_user(
        #     username,
        #     email,
        #     password=password,
            
        # )
        # user.is_admin = True
        # user.save(using=self._db)
        
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None

        if profile is not None:
            # If a UserProfile instance exists, update its user_type field
            profile.user_type = 1
            profile.save()
        else:
            # If a UserProfile instance does not exist, create a new one
            UserProfile.objects.create(
                user=user,
                user_type=1,
            )

        return user

class User(AbstractBaseUser):

    YEAR_OF_STUDY_CHOICES = (
    ('1', 'First Year'),
    ('2', 'Second Year'),
    ('3', 'Third Year'),
    ('4', 'Fourth Year'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=60,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=15)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=250, blank=True, null= True)
    last_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')], blank=True, null= True)
    programme = models.ForeignKey(Programme, to_field='programme_id', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    contact = models.CharField(max_length=250, blank=True, null= True)
    year_of_study = models.CharField(choices=YEAR_OF_STUDY_CHOICES, max_length=1, null=True)


    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


class AcademicTerm(models.Model):
    academic_year = models.CharField(max_length=9, unique=True, help_text="Enter the academic year in the format 'YYYY-YYYY', e.g. '2022-2023'")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"({self.academic_year})"
    
class Semester(models.Model):
    SEMESTER = (
        ('1', 'First Semester'),
        ('2', 'Second Semester')
    )

    semester = models.CharField(choices=SEMESTER, max_length=1)
    academic_year = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('academic_year', 'semester')

    def __str__(self):
        return f"{self.semester}, {self.academic_year}"

class Course(models.Model):
    YEAR_OF_STUDY_CHOICES = (
    ('1', 'First Year'),
    ('2', 'Second Year'),
    ('3', 'Third Year'),
    ('4', 'Fourth Year'),
    )


    SEMESTER = (
        ('1', 'First Semester'),
        ('2', 'Second Semester')
    )
    STATUS = (
        (1, 'Active'),
        (2, 'Inactive')
    )

    course_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
    department = models.ForeignKey(Department, to_field='department_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default = 1, choices=STATUS)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    year_of_study = models.CharField(choices=YEAR_OF_STUDY_CHOICES, max_length=1)
    semester = models.CharField(choices=SEMESTER, max_length=1)



    def __str__(self):
        return self.course_id

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    course = models.ManyToManyField(Course, through='Teaching')
    contact = models.CharField(max_length=250)
    address = models.TextField(blank=True, null = True)
    avatar = models.ImageField(blank=True, null = True, upload_to= 'images/')
    user_type = models.IntegerField(default = 2)
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')], blank=True, null= True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if User.is_staff:
#         if created:
#             UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     print(instance)
#     if User.is_staff:
#         try:
#             lecturer = UserProfile.objects.get(user = instance)
#         except Exception as e:
#             UserProfile.objects.create(user=instance)
#         instance.profile.save()

class Teaching(models.Model):
    lecturer = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
          return f"{self.lecturer} {self.course}"






class StudentProfile(models.Model):
    YEAR_OF_STUDY_CHOICES = (
    ('1', 'First Year'),
    ('2', 'Second Year'),
    ('3', 'Third Year'),
    ('4', 'Fourth Year'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username', on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, through='Enrollment')
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')], blank=True, null= True)
    avatar = models.ImageField(blank=True, null = True, upload_to= 'images/')
    contact = models.CharField(max_length=250, blank=True, null= True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    programme = models.ForeignKey(Programme, to_field='programme_id', on_delete=models.CASCADE)
    year_of_study = models.CharField(choices=YEAR_OF_STUDY_CHOICES, max_length=1)
    
    def __str__(self):
        full_name = self.last_name + ", " + self.first_name
        if self.middle_name:
            full_name += " " + self.middle_name
        return f"{self.student_id}; {full_name}"

# @receiver(post_save, sender=User)
# def create_student_profile(sender, instance, created, **kwargs):
#     if not User.is_staff:
#         if created:
#             StudentProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_student_profile(sender, instance, **kwargs):
#     print(instance)
#     if not User.is_staff:
#         try:
#             student = StudentProfile.objects.get(user = instance)
#         except Exception as e:
#             StudentProfile.objects.create(user=instance)
#         instance.student.save()


class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    def __str__(self):
        # full_name = self.last_name + ", " + self.first_name
        # if self.middle_name:
        #     full_name += " " + self.middle_name
        return f"{self.student} {self.course}"

    def get_present(self):
        student =  self.student
        _course =  self.course
        try:
            present = Attendance.objects.filter(course= _course, student=student, type = 1).count()
            return present
        except:
            return 0
    
    def get_tardy(self):
        student =  self.student
        _course =  self.course
        try:
            present = Attendance.objects.filter(course= _course, student=student, type = 2).count()
            return present
        except:
            return 0

    def get_absent(self):
        student =  self.student
        _course =  self.course
        try:
            present = Attendance.objects.filter(course= _course, student=student, type = 3).count()
            return present
        except:
            return 0
        
class Venue(models.Model):
    venue_id = models.CharField(max_length=15)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    DAY = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday')
    )

    day = models.CharField(choices=DAY, max_length=9)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=200, choices=[('1','Lecture'),('2','Practical'),('3','Tutorial')])
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.day} {self.course}"

class Attendance(models.Model):
    # lecturer
    # semester (at the time or current)
    date = models.DateField(default=timezone.now) #itoke kwenye schedule pia
    course = models.ForeignKey(Course,on_delete=models.CASCADE) #itoke kwenye schedule?
    # student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecturer = models.ManyToManyField(UserProfile, through='InstructorAttendance')
    # type = models.CharField(max_length=250, choices = [('1','Present'),('2','Tardy'),('1','Absent')] )
    # date_updated = models.DateTimeField(auto_now=True)
    # lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(StudentProfile, through='StudentAttendance')
    # is_present = models.BooleanField(default=False)

    def __str__(self):
        return self.course.name + "  " + str(self.date)
    

class StudentAttendance(models.Model):
    lesson = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return str(self.lesson) + "  " + self.student.user.username
    
class InstructorAttendance(models.Model):
    lesson = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return str(self.lesson) + "  " + self.lecturer.user.username

class Report(models.Model):
    #semester in which report is taken
    report_id = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    issued_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class FingerPrintScanner(models.Model):
    scanner_id = models.CharField(max_length=100, unique=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    








    

