from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Custom_User(AbstractUser):
    
    ROLE_CHOICES = (
        ('examiner' , 'Examiner'),
        ('student' , 'Student')
    )
    
    role = models.CharField(max_length = 20 , choices = ROLE_CHOICES)


    def __str__(self):
        return f"{self.username} : ({self.role})"
    