from django.urls import path 
from exam import views

urlpatterns = [
    path('<int:exam_id>/start/' , views.start_exam , name ="start_exam"),
    path('take/<int:submission_id>/', views.take_exam , name = "take_exam"),
    path('result/<int:submission_id>/' , views.exam_result , name = "exam_result"),
    path('<int:exam_id>/upload/' , views.upload_questions , name = "upload_question"),
    path('<int:exam_id>/upload/success/', views.upload_success, name= "upload-success"),
    path('dashboard/' , views.student_dashboard , name = "student_dashboard"),
    path('examiner/dashboard/' , views.examiner_dashboard , name = 'examiner_dashboard'),
    path('examiner/exam/<int:exam_id>/submissions/' , views.examiner_exam_submissions , name="examiner_exam_submissions"),
]
