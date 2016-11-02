from django import forms
from django.contrib.auth.models import User
from backend.models import *
import csv
class Register(forms.Form):
	# class Meta:
	# 	model = User
	# 	fields = ['first_name', 'last_name', 'email', 'username']
	# password = forms.CharField(label="Password", widget=forms.PasswordInput())
	# password2 = forms.CharField(label="Re enter Password", widget=forms.PasswordInput())	
	first_name = forms.CharField(label="First Name", max_length=30)
	last_name = forms.CharField(label="Last Name", max_length=30)
	email = forms.EmailField()
	username = forms.CharField(label="Username", max_length=30)
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
	password2 = forms.CharField(label="Re enter Password", widget=forms.PasswordInput())
	# user = User(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
	# user.save()

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Passwords do not match")
		return self.cleaned_data

	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError("Username already exists. Try another.")
		return self.cleaned_data['username']
			
		# try:
		# 	user = User.objects.get(username__iexact=self.cleaned_data['username'])
		# except Instructor.DoesNotExist:
		# 	return self.cleaned_data['username']
		# raise forms.ValidationError("Username already exists. Try another.")
class CreateFeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ['course', 'topic', 'due_date']
	original_field = forms.CharField(label='Question 1', max_length=50)
	added_field_count = forms.CharField(widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
		added_fields = kwargs.pop('added', 0)
		super(CreateFeedbackForm, self).__init__(*args, **kwargs)
		self.fields['added_field_count'].initial = added_fields
		for index in range(int(added_fields)):
			self.fields['added_field_{index}'.format(index=index)] = \
				forms.CharField(label='Question {index}'.format(index=index), max_length=50)



# class StudentRegister(forms.ModelForm):
# 	class Meta:
# 		model = Student
# 		fields = ['LDAP_id','password', 'firstname', 'lastname', 'course']

class AdminLogin(forms.Form):
	username = forms.CharField(label="Username", max_length=30)
	password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput())

class CourseRegister(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['code', 'name', 'semester', 'instructor', 'midsem_date', 'endsem_date']

class CourseAssign(forms.Form):
	code = forms.CharField(max_length=5)
	instructor = forms.CharField(max_length=30)

class DeadlineForm(forms.ModelForm):
	class Meta:
		model = Deadline
		fields = ['due_date', 'topic', 'description', 'course']

class UploadStudentList(forms.Form):
	file = forms.FileField()
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