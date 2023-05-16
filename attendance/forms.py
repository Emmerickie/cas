from re import T
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django import forms
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.models import User
from attendance.models import Enrollment, UserProfile, Department, Course, StudentProfile, Programme, User

class UserRegistration(UserCreationForm):
    email = forms.EmailField(max_length=250,help_text="The email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.") 
    department = forms.ModelChoiceField(queryset=Department.objects.all())
   

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'middle_name', 'last_name', 'gender', 'department', 'contact')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['contact'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        # self.fields['programme'].widget.attrs.update({'class': 'form-control'})
    
    

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} already exists")

class StudentRegistration(UserCreationForm):
    # email = forms.EmailField(max_length=250,help_text="The email field is required.")
    # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    # middle_name = forms.CharField(required=True) 
    # contact =  forms.CharField(required=True)
    # gender = forms.TypedChoiceField(initial=None, choices=[('Male','Male'),('Female','Female')])
    # programme = forms.ModelChoiceField(queryset=Programme.objects.all())

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'middle_name', 'last_name', 'gender', 'programme', 'year_of_study', 'contact')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['contact'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['programme'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_of_study'].widget.attrs.update({'class': 'form-control'})


    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} already exists")
    
    # def save(self, commit=True):
    #     # user_id = self.cleaned_data.get('user_id')
    #     # user = User.objects.get(id=user_id)
    #     user = super().save(commit=False)
    #     user.set_password((self.cleaned_data['last_name']).upper())

    #     if commit:
    #         user.save()
            

        # student_profile = StudentProfile.objects.create(ins
        #     user=user,
        #     student_id=self.cleaned_data['username'],
        #     first_name=self.cleaned_data['first_name'],
        #     middle_name=self.cleaned_data['middle_name'],
        #     last_name=self.cleaned_data['last_name'],
        #     gender=self.cleaned_data['gender'],
        #     contact=self.cleaned_data['contact'],
        #     programme=self.cleaned_data['programme']
        # )
        
        # return student_profile
    

class StudentProfileForm(forms.ModelForm):
    # user = forms.IntegerField()
    # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    # middle_name = forms.CharField(required=True)

    class Meta:
        model = StudentProfile
        fields = ('gender', 'programme', 'contact')


class EnrollForm(forms.Form):
    # programme = forms.ModelChoiceField(queryset=Programme.objects.all())
    student = forms.ModelChoiceField(queryset=StudentProfile.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'programme' in self.data:
    #         self.fields['student'].queryset = StudentProfile.objects.filter(programme=self.data['programme'])
    #     # elif self.instance.pk:
    #     #     self.fields['student'].queryset = self.instance.programme.student_set.all()
    
    



class UpdateFaculty(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The username field is required.")
    email = forms.EmailField(max_length=250,help_text="The email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
        

    def __init__(self, user= None,*args, **kwargs):
        self.user = user
        super(UpdateFaculty, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id= self.user.id).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        print(self.user.id)
        try:
            user = User.objects.exclude(id= self.user.id).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")
    

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()
    is_staff = forms.BooleanField()

    class Meta:
        model = User
        fields = ["email", "password", "is_staff", "is_active", "is_admin"]




class UpdateProfileMeta(forms.ModelForm):
    dob = forms.DateField(help_text="The Birthday field is required.")
    contact = forms.CharField(max_length=250,help_text="The Contact field is required.")
    address = forms.CharField(help_text="The Contact field is required.")

    class Meta:
        model = UserProfile
        fields = ('dob', 'contact', 'address','gender','department','avatar')

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')

class UpdateProfileAvatar(forms.ModelForm):
    avatar = forms.ImageField(help_text="The Avatar field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = UserProfile
        fields = ('avatar',)
    
    def __init__(self,*args, **kwargs):
        self.user = kwargs['instance']
        kwargs['instance'] = self.user.profile
        super(UpdateProfileAvatar,self).__init__(*args, **kwargs)

    def clean_current_password(self):
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError("Password is Incorrect")

class AddAvatar(forms.ModelForm):
    avatar = forms.ImageField(help_text="The Avatar field is required.")
    class Meta:
        model = UserProfile
        fields = ('avatar',)

class SaveDepartment(forms.ModelForm):
    department_id = forms.CharField(max_length=100,help_text = "Department id Field is required.")
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 300px'}))

    class Meta:
        model= Department
        fields = ('department_id', 'name', 'status')

class SaveCourse(forms.ModelForm):
    # code = forms.CharField(max_length=30)
    # name = forms.CharField(max_length=100,help_text = "Course name Field is required.")
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model= Course
        fields = ('course_id', 'name', 'year_of_study', 'semester', 'department', 'status')

    # def clean_department(self):
    #     department = self.cleaned_data['department']
    #     try:
    #         dept = Department.objects.get(department_id = department)
    #         return dept
    #     except:
    #         raise forms.ValidationError(f'Department value is invalid.')

    # def clean_name(self):
    #     id = self.instance.id if not self.instance == None else 0
    #     try:
    #         if id.isnumeric() and id > 0:
    #             course = Course.objects.exclude(id = id).get(name = self.cleaned_data['name'])
    #         else:
    #             course = Course.objects.get(name = self.cleaned_data['name'])
    #     except:
    #         return self.cleaned_data['name']
    #     raise forms.ValidationError(f'{course.name} course Already Exists.')

class SaveProgramme(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    # school_year = forms.CharField(max_length=250,help_text = "School Year Field is required.")
    # level = forms.CharField(max_length=250,help_text = "Level Field is required.")
    name = forms.CharField(max_length=250,help_text = "Class Name Field is required.",widget=forms.TextInput(attrs={'style': 'width: 300px'}))

    class Meta:
        model= Programme
        fields = ('department', 'programme_id', 'name')

    # def clean_assigned_faculty(self):
    #     assigned_faculty = self.cleaned_data['assigned_faculty']
    #     try:
    #         dept = UserProfile.objects.get(id = assigned_faculty)
    #         return dept
    #     except:
    #         raise forms.ValidationError(f'Assigned Faculty value is invalid.')

class SaveStudent(forms.ModelForm):
    # programme = forms.ModelChoiceField(queryset=Programme.objects.all())


    class Meta:
        model = StudentProfile
        fields = ('student_id','first_name','middle_name','last_name','gender','programme','contact')
    
    # def clean_student_code(self):
    #     code = self.cleaned_data['student_code']
    #     try:
    #         if not self.instance.id is None:
    #             student = Student.objects.exclude(id = self.instance.id).get(student_code = code)
    #         else:
    #             student = Student.objects.get(student_code = code)
    #     except:
    #         return code
    #     raise forms.ValidationError(f"Student Code {code} already exists.")

    # def clean_course(self):
    #     cid = self.cleaned_data['course']
    #     try:
    #         course = Course.objects.get(id = cid)
    #         return course
    #     except:
    #         raise forms.ValidationError("Invalid Course Value")

class SaveClassStudent(forms.ModelForm):
    classIns = forms.IntegerField()
    student = forms.IntegerField()

    class Meta:
        model = Enrollment
        fields = ('course','student')

    def clean_classIns(self):
        cid = self.cleaned_data['classIns']
        try:
            classIns = Class.objects.get(id = cid)
            return classIns
        except:
            raise forms.ValidationError("Class ID is Invalid.")
    
    def clean_student(self):
        student_id = self.cleaned_data['student']
        _class = Class.objects.get(id = self.data.get('classIns'))
        student = Student.objects.get(id = student_id)
        try:
            cs = Enrollment.objects.get(classIns = _class, student = student)
            if len(cs) > 0:
                raise forms.ValidationError(f"Student already exists in the Class List.")
        except:
            return student
