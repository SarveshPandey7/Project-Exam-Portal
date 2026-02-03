from django.contrib import admin
from exam.models import Exam , Question , ExamSet , SetQuestion

# Register your models here.

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(ExamSet)
admin.site.register(SetQuestion)