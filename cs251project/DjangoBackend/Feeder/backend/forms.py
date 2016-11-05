from django import forms
from django.contrib.auth.models import User
from backend.models import *
import csv
class Register(forms.Form):
	first_name = forms.CharField(label="First Name", max_length=30)
	last_name = forms.CharField(label="Last Name", max_length=30)
	email = forms.EmailField()
	username = forms.CharField(label="Username", max_length=30)
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
	password2 = forms.CharField(label="Re enter Password", widget=forms.PasswordInput())

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Passwords do not match")
		return self.cleaned_data

	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError("Username already exists. Try another.")
		return self.cleaned_data['username']
			
class CreateFeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ['course', 'topic', 'due_date']
	def __init__(self, *args, **kwargs):
		super(CreateFeedbackForm, self).__init__(*args, **kwargs)
		self.fields['topic'].widget.attrs={'placeholder': 'Topic'}
		self.fields['due_date'].widget.attrs={'placeholder': 'YYYY-MM-DD'}
	# question = forms.CharField(max_length=100, label="Rating Question 1", widget=forms.TextInput(attrs={'placeholder': 'Question', 'class':'form-control'}))

class AdminLogin(forms.Form):
	username = forms.CharField(label="Username", max_length=30)
	password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput())

class CourseRegister(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['code', 'name', 'semester', 'instructor', 'midsem_date', 'endsem_date']
	# file = forms.FileField()
	def __init__(self, *args, **kwargs):
		super(CourseRegister, self).__init__(*args, **kwargs)
		self.fields['midsem_date'].widget.attrs={'placeholder': 'YYYY-MM-DD'}
		self.fields['endsem_date'].widget.attrs={'placeholder': 'YYYY-MM-DD'}

class CourseAssign(forms.Form):
	code = forms.CharField(max_length=5)
	instructor = forms.CharField(max_length=30)

class DeadlineForm(forms.ModelForm):
	class Meta:
		model = Deadline
		fields = ['due_date', 'topic', 'description', 'course']
	def __init__(self, *args, **kwargs):
		super(DeadlineForm, self).__init__(*args, **kwargs)
		self.fields['due_date'].widget.attrs={'placeholder': 'YYYY-MM-DD'}

class UploadStudentList(forms.Form):
	file = forms.FileField()
	course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)
	# def clean(self):
	# 	file = self.cleaned_data['file']
	# 	data = csv.reader(file)
	# 	for row in data:
	# 		student = Student(LDAP=row[0], name=row[1], password=row[2])
	# 		student.save()
	# def save():
		# data = csv.reader(self.cleaned_data['file'])
		# with open(getF()) as f:

# class FeedbackForm(forms.ModelForm):
	
# 	self.question_set()
    # yes_no = forms.ChoiceField(
    #     choices=,
    #     initial=1,
    #     widget=forms.RadioSelect(attrs={'class': 'can_reveal_input'}),
    #     label="Are you happy with Our service?"
    # )
    # comments = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'class': 'hidden', 'placeholder': 'Leave us your comments...'
    #     }),
    #     required=False,
    #     label=""
    # )

	# class Meta:
	# 	model = User
	# 	fields = ['first_name', 'last_name', 'email', 'username']
	# password = forms.CharField(label="Password", widget=forms.PasswordInput())
	# password2 = forms.CharField(label="Re enter Password", widget=forms.PasswordInput())	
	# user = User(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
	# user.save()
		
		# try:
		# 	user = User.objects.get(username__iexact=self.cleaned_data['username'])
		# except Instructor.DoesNotExist:
		# 	return self.cleaned_data['username']
		# raise forms.ValidationError("Username already exists. Try another.")
# class StudentRegister(forms.ModelForm):
# 	class Meta:
# 		model = Student
# 		fields = ['LDAP_id','password', 'firstname', 'lastname', 'course']