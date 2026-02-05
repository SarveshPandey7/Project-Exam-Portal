from django.shortcuts import render , redirect , get_object_or_404
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseForbidden
from exam.forms import QuestionUploadForm
from exam.services import upload_question_from_excel , generate_exam_set
from exam.models import Exam , SetQuestion , Question
from submission.models import Submission , StudentAnswer
from django.utils import timezone
from datetime import timedelta

# Create your views here.

@login_required
def start_exam(request , exam_id):
    exam = get_object_or_404(Exam , id = exam_id)
    
    if exam.status != Exam.STATUS_LIVE:
        return render(request , 'exam/exam_not_available.html' , {'exam' : exam})
    
    #to check is student has previously submitted or not
    submission = Submission.objects.filter(
        student = request.user ,
        exam = exam
    ).first()
    
    if submission:
        #true ,  means already attempted.
        return redirect('take_exam' , submission_id = submission.id)
    
    #if not , assign a random set to student
    exam_set =  random.choice(list(exam.sets.all()))
    
    #creating the new submission
    submission = Submission.objects.create(
        student = request.user , 
        exam = exam,
        exam_set = exam_set,
        score = 0,
    )
    
    return redirect('take_exam' , submission_id = submission.id)


@login_required
def take_exam(request , submission_id):
    submission = get_object_or_404(
        Submission ,
        id=submission_id ,
        student = request.user
    )
    
     #for timer and auto submit
    exam = submission.exam
    #status must be live
    if exam.status != Exam.STATUS_LIVE:
        return redirect('student_dashboard')
    
    end_time = submission.started_at + timedelta(
            minutes = exam.duration_minutes
        )
    
    is_time_over = timezone.now() >= end_time
    already_submitted = submission.answers.exists()
        
    remaining_seconds = int(
            (end_time - timezone.now()).total_seconds()
            )
    
        
        #time reaches end
    if remaining_seconds <= 0:
        if not submission.answers.exists():
            #auto submit ,  and half answers will be marked zero
            submission.score = 0
            submission.save()

        return redirect('exam_result' , submission_id=submission.id)
    
    set_questions = SetQuestion.objects.filter(
        exam_set = submission.exam_set
    ).select_related('question')
    
                
    #to prevent resubmisson
    if request.method == 'POST':
        if submission.answers.exists():
            return redirect('exam_result' , submission_id = submission.id)

        if already_submitted or is_time_over:
            return redirect('exam_result', submission_id=submission.id)
        
        #if not
        score = 0
        
        for set_question in set_questions:
            selected = request.POST.get(f"question_{set_question.question.id}")
            if not selected:
                continue
            
            selected = selected.strip().upper()
            StudentAnswer.objects.create(
                submission = submission,
                question = set_question.question,
                select_option = selected,
            )
            
            if selected == set_question.question.correct_option:
                #add marks for each correct answer
                score += set_question.question.marks
                
        submission.score = score
        submission.save()
        
        return redirect('exam_result' , submission_id = submission.id)
    
    return  render(request , 'exam/take_exam.html' , {
        'submission' : submission,
        'set_questions' : set_questions,
        'remaining_seconds':remaining_seconds,
        'already_submitted' : already_submitted,
    })
    
    
@login_required
def exam_result(request , submission_id):
    submission = get_object_or_404(
        Submission,
        id = submission_id,
        student = request.user
    )
    
    answers = StudentAnswer.objects.filter(
        submission=submission
    ).select_related('question')

    answer_map = {
        ans.question_id: ans.select_option
        for ans in answers
    }

    set_questions = SetQuestion.objects.filter(
        exam_set=submission.exam_set
    ).select_related('question')

    result_data = []

    for set_ques in set_questions:
        selected = answer_map.get(set_ques.question.id)
        correct = set_ques.correct_option

        result_data.append({
            'question': set_ques.question,
            'selected': selected,
            'correct': correct,
            'is_correct': selected == correct,
            'marks': set_ques.question.marks if selected == correct else 0
        })
    
    return render(request , 'exam/result.html' , {
        'submission' : submission ,
        'result_data' : result_data,
        })


@login_required
def upload_questions(request , exam_id):
    exam = get_object_or_404(Exam , id = exam_id)
    
    if exam.status != Exam.STATUS_DRAFT:
        return render(request , 'exam/exam_locked.html' , {'exam' : exam})
    
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST , request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            Question.objects.filter(exam=exam).delete()
            upload_question_from_excel(file , exam)
            generate_exam_set(exam)
            return redirect('upload_success' , exam_id = exam.id)
        
    else:
        form = QuestionUploadForm()
        
    return render(request , 'exam/upload.html' , {'form' : form , 'exam' : exam})

@login_required
def upload_success(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    return render(request, 'exam/upload_success.html', {'exam': exam})

@login_required
def student_dashboard(request):
    exams = Exam.objects.all()
    
    submissions = Submission.objects.filter(student = request.user)
    
    #map the submissions
    submission_map = {
        sub.exam_id: sub for sub in submissions
    }
    
    dashboard_data = []#empty list to store data
    
    for exam in exams:
        submission = submission_map.get(exam.id)
        
        dashboard_data.append({
            'exam' : exam ,
            'submission' : submission ,
            'attempted' : submission is not None
        })
        
    return render(request , 'exam/dashboard.html' , {'dashboard_data' : dashboard_data})

@login_required
def examiner_dashboard(request):
    exams = Exam.objects.filter(created_by = request.user)
    
    return render(request , 'exam/examiner_dashboard.html' , {'exams' : exams})


def examiner_exam_submissions(request , exam_id):
    exam = get_object_or_404(Exam , id = exam_id)
    
    if exam.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to view this Exam")
    
    submissions  = Submission.objects.filter(
        exam=exam,
    ).select_related('student')
    
    return render(request , 'exam/examiner_submissions.html' , {
        'exam': exam,
        'submissions' : submissions,
    })