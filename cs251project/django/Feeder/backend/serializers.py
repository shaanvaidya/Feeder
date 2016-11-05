from rest_framework import serializers
from .models import *

class DeadlineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Deadline
		fields = ('topic','due_date','description')

class RatingQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = RatingQuestion
		fields = ('q',)

class SubjectiveQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = SubjectiveQuestion
		fields = ('q',)

class FeedbackSerializer(serializers.ModelSerializer):
	ratingquestion_set = RatingQuestionSerializer(many=True, read_only=True)
	subjectivequestion_set = SubjectiveQuestionSerializer(many=True, read_only=True)
	class Meta:
		model = Feedback
		fields = ('topic', 'due_date', 'ratingquestion_set', 'subjectivequestion_set')

class CourseSerializer(serializers.ModelSerializer):
	deadline_set = DeadlineSerializer(many=True, read_only=True)
	feedback_set = FeedbackSerializer(many=True, read_only=True)
	class Meta:
		model = Course
		fields = ('code','name','midsem_date','endsem_date','deadline_set', 'feedback_set')

class StudentSerializer(serializers.ModelSerializer):
	course = CourseSerializer(many=True, read_only=True)
	class Meta:
		model = Student
		fields = ('LDAP','password','name','logged_in','course')