from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(MyAdmin)
admin.site.register(Deadline)
admin.site.register(Feedback)
admin.site.register(RatingQuestion)
admin.site.register(SubjectiveQuestion)
admin.site.register(RatingQuestionResponse)
admin.site.register(SubjectiveQuestionResponse)