from django.db import models
from django.conf import settings
from exam.models import Exam , ExamSet , Question

# Create your models here.

User = settings.AUTH_USER_MODEL

class Submission(models.Model):
    
    student = models.ForeignKey(User , on_delete=models.CASCADE , related_name='submission')
    exam = models.ForeignKey(Exam , on_delete=models.CASCADE , related_name='submission')
    exam_set = models.ForeignKey(ExamSet , on_delete=models.CASCADE)
    
    score = models.PositiveIntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        #single attempt per user
        unique_together = ('student' , 'exam')
        
    def __str__ (self):
        return f"{self.student} - {self.exam}"
    
    
class StudentAnswer(models.Model):
    
    submission = models.ForeignKey(Submission , on_delete=models.CASCADE , related_name='answers')
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    select_option = models.CharField(max_length=1 , choices=[('A' , 'A') , ('B' , 'B') , ('C' , 'C') , ('D' ,'D')])
    
    class Meta:
        unique_together = ('submission' , 'question')
        
    def __str__ (self):
        return f"{self.submission} - {self.question.id}"

