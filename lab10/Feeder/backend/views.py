from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from backend.forms import *
from backend.models import *
from django.contrib import messages
import csv
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
import json
from .serializers import *
from datetime import datetime
# from django.utils import simplejson
# from itertools import chain
secretkey = "MeraNaamJoker"

@login_required(login_url="login/")
def home(request):
	if request.method == 'POST':
		form = DeadlineForm(request.POST, request.FILES)
		if form.is_valid():
			deadline = form.save(commit=False)
			deadline.save()
			return HttpResponseRedirect('/')
	else:
		form = DeadlineForm()
	deadlines = Deadline.objects.all()
	upcoming = []
	finished = []
	for deadline in deadlines:
		if deadline.due_date > datetime.now():
			upcoming.append(deadline.pk)
		else:
			finished.append(deadline.pk)
	upcomingdeadlines = Deadline.objects.filter(pk__in=upcoming)
	finisheddeadlines = Deadline.objects.filter(pk__in=finished)
	courses = Course.objects.all()
	c = {'form':form, 'upcomingdeadlines':upcomingdeadlines, 'finisheddeadlines':finisheddeadlines,'courses':courses}
	return render(request, 'home.html', c)

@login_required(login_url="login/")
def createfeedbackform(request):
	if request.method == 'POST':
		form = CreateFeedbackForm(request.POST)
		countrating = request.POST.get('countrating')
		countsubjective = request.POST.get('countsubjective')
		if form.is_valid():

			# feedback = Feedback(
			# 	course = Course.objects.get(id=request.POST['course']),
			# 	topic = request.POST['topic'],
			# 	due_date = request.POST['due_date'],
			# )	
			feedback = form.save(commit=True)
			feedback.save()
			question = RatingQuestion(q=request.POST['question'], feedback=feedback)
			question.save()
			for i in range(int(countrating)):
				question = RatingQuestion(q=request.POST['question_{}'.format(i+2)], feedback=feedback)
				question.save()
			for i in range(int(countsubjective)):
				question = SubjectiveQuestion(q=request.POST['question_{}'.format(i+2)], feedback=feedback)
				question.save()
			return HttpResponseRedirect('/createfeedbackform')
	else:
		form = CreateFeedbackForm()
	return render(request, 'createfeedback.html', {'form':form})

#########Implementation 1#################################
# def createfeedbackform(request):
# 	if request.method == 'POST':
# 		form = CreateFeedbackForm(request.POST, added=request.POST.get('added_field_count'))
# 		added = request.POST.get('added_field_count')
# 		if form.is_valid():
# 			# feedback = Feedback(
# 			# 	course = request.POST['course'],
# 			# 	topic = request.POST['topic'],
# 			# 	due_date = request.POST['due_date']
# 			# )
# 			feedback = form.save(commit=True)
# 			feedback.save()
# 			ques = Question(q=request.POST['original_field'], feedback=feedback)
# 			ques.save()
# 			# feedback.save()
# 			for i in range(int(added)):
# 				ques = Question(q=request.POST['added_field_{i}'.format(i=i)], feedback=feedback)
# 				ques.save()
# 			return HttpResponseRedirect('/createfeedbackform')
# 	else:
# 		form = CreateFeedbackForm()
# 		return render(request, 'createfeedback.html', { 'form': form })
#########################################################################

@csrf_protect
def register(request):
	if request.method == 'POST':
		form = Register(request.POST, request.FILES)
		if form.is_valid():
			user = User(
				first_name = request.POST['first_name'],
				last_name = request.POST['last_name'],
				username = request.POST['username'],
				email = request.POST['email'],
			)
			user.set_password(request.POST['password1'])
			user.save()
			return HttpResponseRedirect('/success')
	else:
		form = Register()
		c = {'form': form}
		return render(request, 'registration/register.html', c)

def registersuccess(request):
	return render(request,'registration/success.html')

def adminlogin(request):
	admin = MyAdmin.objects.get(username="admin")
	if admin.logged_in == False:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			if MyAdmin.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
				admin = MyAdmin.objects.get(username=request.POST['username'], password=request.POST['password'])
				admin.logged_in = True
				admin.save()
				return HttpResponseRedirect('/adminhome')
			else:
				messages.error(request, "Admin not recognised")
				return HttpResponseRedirect('/adminhome')			
		else:
			form = AdminLogin()
			c = {'form': form}
			return render(request, 'admin/adminlogin.html', c)
	else:
		return HttpResponseRedirect('/adminhome')			

@csrf_protect
def adminhome(request):
	admin = MyAdmin.objects.get(username="admin")
	if admin.logged_in:
		if request.method == 'POST':
			if request.POST['action'] == "Add Course":	
				form = CourseRegister(request.POST, request.FILES)
				if form.is_valid():
					course = form.save(commit = True)
					midsem_deadline = Deadline(due_date=course.midsem_date, topic="Midsemester Examination", course=course)
					midsem_deadline.save()
					endsem_deadline = Deadline(due_date=course.endsem_date, topic="Endsemester Examination", course=course)
					endsem_deadline.save()
					question1 = "The course content was intelectually stimulating"
					question2 = "Textbooks and/or other references were easily available"
					midsem_feedback = Feedback(course=course, due_date=course.midsem_date, topic="Midsem Feedback")
					endsem_feedback = Feedback(course=course, due_date=course.endsem_date, topic="Endsem Feedback")
					midsem_feedback.save()
					endsem_feedback.save()
					ques = RatingQuestion(q=question1, feedback=midsem_feedback)
					ques.save()
					ques = RatingQuestion(q=question2, feedback=midsem_feedback)
					ques.save()
					ques = RatingQuestion(q=question1, feedback=endsem_feedback)
					ques.save()
					ques = RatingQuestion(q=question2, feedback=endsem_feedback)
					ques.save()
					course.save()
					return HttpResponseRedirect('/adminhome')
			elif request.POST['action'] == "Upload":
				form = UploadStudentList(request.POST, request.FILES)
				if form.is_valid():
					uploaded_file = request.FILES['file']
					with open("/tmp/%s" %uploaded_file.name, 'wb') as fout:
						for chunk in uploaded_file.chunks():
							fout.write(chunk)
					reader = csv.reader(open('/tmp/%s' %uploaded_file.name))
					for row in reader:
						student = Student(LDAP = row[0], name = row[1], password = row[2])
						student.save()
					return HttpResponseRedirect('/adminhome')
		else:
			form = CourseRegister()
			formupload = UploadStudentList()
			courses = Course.objects.all()
			c = {'form':form, 'courses': courses, 'formupload': formupload}
			return render(request, 'admin/adminhome.html', c)
	else:
		return HttpResponseRedirect('/adminlogin')

def adminlogout(request):
	admin = MyAdmin.objects.get(username="admin")
	if admin.logged_in:
		admin.logged_in = False
		admin.save()
	return HttpResponseRedirect('/adminlogin')

@api_view(['POST'])
def studentlogin(request):
	# secret = request.data['secretkey']
	LDAP = request.data['LDAP']
	password = request.data['password']
	# if secret != secretkey:
	# 	return JsonResponse({'status':"Not Authorised"})
	# else:
	try:
		stu = Student.objects.get(LDAP=LDAP)
		courses = stu.course.all()
		# x = serializers.serialize(courses)
		# x = StudentSerializer([stu,], many=True)
		x = CourseSerializer(courses, many=True)
		# json_data = json.dumps( {'student':a, 'courses':b }, default=json_serial )
	except Student.DoesNotExist:
		return HttpResponse(status=201)
		# return JsonResponse({'status':"Invalid LDAP id"})
	if password != stu.password:
		return HttpResponse(status=201)
		# return JsonResponse({'status':'Incorrect Password'})
	else:
		stu.logged_in = True
		stu.save()
		return JsonResponse(x.data, safe=False)
		# return JsonResponse({'status':"Success", 'name':name, 'logged_in':student.logged_in})
# @api_view(['POST'])
# def studentlogout(request):
# 	LDAP = request.data['LDAP']
# 	try:
# 		student = Student.objects.get(LDAP=LDAP)
# 	except Student.DoesNotExist:
# 		return HttpResponse(status=400)


################Implementation 2#####################
# def createfeedbackform(request):
# 	if request.method == 'POST':
# 		if request.POST['action'] == "+":
# 			extra = int(float(request.POST['extra'])) + 1
# 			form = CreateFeedbackForm(initial=request.POST)
# 			extrafields= formset_factory(ExtraFields, extra=extra)
# 		else:
# 			extra = int(float(request.POST['extra']))
# 			form = CreateFeedbackForm(request.POST)
# 			extrafields = formset_factory(ExtraFields, extra=extra)(request.POST)

# 			if form.is_valid() and extrafield.is_valid():
# 				if request.POST['action'] == "Create":
# 					for extrafield in extrafields:
# 						if not extrafield.cleaned_data['delete']:
# 						    # create data
# 				elif request.POST['action'] == "Edit":
# 					for extrafield in extrafields:
# 						if extrafield.cleaned_data['delete']:
#     						# delete data
# 						else:
#     						# create data
# 				return HttpResponseRedirect('abm_usuarios')
#     else:
# 		form = SpecificForm()
# 		extra = 1
# 		formset = formset_factory(FormsetForm, extra=extra)

# 		template = loader.get_template('some_template.html')
# 		context = RequestContext(request, {
# 		   # some context
# 		})
# 		return HttpResponse(template.render(context))
