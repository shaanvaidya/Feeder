from django.db import models
from django.contrib.auth.models import User

# class Instructor(models.Model):
# 	username = models.CharField(max_length=30, primary_key=True)
# 	password = models.CharField(max_length=30)
# 	first_name = models.CharField(max_length=30)
# 	last_name = models.CharField(max_length=30)
# 	email = models.EmailField()
# 	def __str__(self):
# 		return self.username

class MyAdmin(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	logged_in = models.BooleanField(default=False)
	def __str__(self):
		return self.username

class Course(models.Model):
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=30)
	semester = models.CharField(max_length=30)
	instructor = models.ForeignKey(User, on_delete=models.CASCADE)
	midsem_date = models.DateTimeField()
	endsem_date = models.DateTimeField()
	def __str__(self):
		return self.code

class Student(models.Model):
	LDAP = models.CharField(null=True, max_length=9)
	password = models.CharField(max_length=30)
	name = models.CharField(max_length=50)
	course = models.ManyToManyField(Course, blank=True)
	logged_in = models.BooleanField(default=False)
	def __str__(self):
		return self.LDAP

class Deadline(models.Model):
	due_date = models.DateTimeField()
	topic = models.CharField(max_length=30)
	description = models.TextField(default="")
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Feedback(models.Model):
	topic = models.CharField(max_length=30)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	due_date = models.DateTimeField()

class Question(models.Model):
	q = models.CharField(max_length=50)
	ratings = (
		(1, "Strongly Agree"),
		(2, 'Agree'),
		(3, 'Neutral'),
		(4, 'Disagree'),
		(5, "Strongly Disagree"),
	)
	opinion = models.IntegerField(choices=ratings, default=1)
	feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)

# class FeedbackForm(forms.Form):
#     yes_no = forms.ChoiceField(
#         choices=,
#         initial=1,
#         widget=forms.RadioSelect(attrs={'class': 'can_reveal_input'}),
#         label="Are you happy with Our service?"
#     )
#     comments = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'hidden', 'placeholder': 'Leave us your comments...'
#         }),
#         required=False,
#         label=""
#     )