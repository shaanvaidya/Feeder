from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
	# student = StudentSerializer(many=True)
	# code = serializers.CharField(max_length=5)
	# name = serializers.CharField(max_length=30)
	# midsem_date = serializers.DateTimeField()
	# endsem_date = serializers.DateTimeField()

	class Meta:
		model = Course
		fields = ('code','name','midsem_date','endsem_date')

class StudentSerializer(serializers.ModelSerializer):
	course = CourseSerializer(many=True, read_only=True)
	class Meta:
		model = Student
		fields = ('LDAP','password','name','logged_in','course')

class DeadlineSerializer(serializers.ModelSerializer):
	course = CourseSerializer(many=True, read_only=True)
	class Meta:
		model = Deadline
		fields = ('topic','due_date','description')
