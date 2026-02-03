from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Exam(models.Model):
    STATUS_DRAFT = 'DRAFT'
    STATUS_LIVE = 'LIVE'
    STATUS_CLOSED = 'CLOSED'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT , 'Draft'),
        (STATUS_LIVE , 'Live'),
        (STATUS_CLOSED , 'Closed')
    ]
    
    title = models.CharField(max_length=200)
    decription = models.TextField(blank=True)
    created_by = models.ForeignKey(User , on_delete = models.CASCADE , related_name= 'created_exams')
    total_marks = models.PositiveIntegerField()
    
    status = models.CharField(
        max_length = 10,
        choices = STATUS_CHOICES,
        default = STATUS_DRAFT
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    duration_minutes = models.PositiveIntegerField(help_text= "Duration of exam in minutes")
    
    def __str__(self):
        return f"{self.title}"
    

class Question(models.Model):
    exam = models.ForeignKey(Exam , on_delete = models.CASCADE , related_name = 'questions')
    question_text = models.TextField()
    
    option_a = models.CharField(max_length=250) 
    option_b = models.CharField(max_length=250) 
    option_c = models.CharField(max_length=250) 
    option_d = models.CharField(max_length=250)
    
    correct_option = models.CharField(
        max_length=1 ,
        choices=[
            ('A' , 'A') ,
            ('B' , 'B') ,
            ('C' , 'C') , 
            ('D' , 'D')
            ])
    
    marks = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.question_text[:50] 
    
    
#will run for each set    
class ExamSet(models.Model):
    SET_CHOICES = (
        ('A' , 'Set A'),
        ('B' , 'Set B'),
        ('C' , 'Set C'),
        ('D' , 'Set D'),
    )
    
    exam = models.ForeignKey(Exam , on_delete = models.CASCADE , related_name = 'sets')
    set_code = models.CharField(max_length=1 , choices=SET_CHOICES)
    
    def __str__(self):
        return f"{self.exam.title} : {self.set_code}"
    
    
class SetQuestion(models.Model):
    exam_set = models.ForeignKey(ExamSet , on_delete=models.CASCADE , related_name='set_questions')
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    
    correct_option = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D')
        ]
    )
    
    order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('exam_set' , 'question')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exam_set} - Q{self.question.id}"