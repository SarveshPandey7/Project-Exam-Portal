import random , pandas as pd
from exam.models import ExamSet , SetQuestion , Question
from django.db import transaction

#function to create 4 random sets A , B , C , D

@transaction.atomic #if an error occured  , nothing is saved
def generate_exam_set(exam):
    if exam.status != exam.STATUS_DRAFT:
        raise ValueError("Cannnot generate Question sets unless exam is not in DRAFT state")
    
    #all the questions on current exam will be passed to questions
    questions = list(Question.objects.filter(exam=exam))
    
    if(len(questions) == 0):
        raise ValueError("No Questions Found!")
    
    #creating list of set codes
    set_codes = ['A' , 'B' , 'C' , 'D']
    
    #deletes old data
    ExamSet.objects.filter(exam=exam).delete()
    
    #we have set_code in models.py for ExamSet
    for set_code in set_codes:
        exam_set , created = ExamSet.objects.create(exam=exam , set_code=set_code)
        
        #shadow copy of questions
        shuffled_questions = questions [:]
        random.shuffle(shuffled_questions)
        
        #to clean old data id examiner adds a new data or regenerates the set
        SetQuestion.objects.filter(exam_set=exam_set).delete()
        
        
        #for ordering
        for order , question in enumerate(shuffled_questions , start = 1):
            #storing the details in db
            SetQuestion.objects.create(
                exam_set=exam_set,
                question=question,
                order=order,
                correct_option = question.correct_option,
            )

         
         
#function to deal with excel file uploads
def upload_question_from_excel(file , exam):
    dataFile = pd.read_excel(file)
    
    #to check correct format for excel sheet (using sets)
    required_columns = {
        'question_text' ,
         'option_a',
         'option_b',
         'option_c',
         'option_d',
         'correct_option',
         'marks'
    }
    
    if not required_columns.issubset(dataFile.columns):
        missing = required_columns - set(dataFile.columns)
        raise ValueError(f"missing fields : {missing}")
    
    questions = [] #questions list to add questions from excel to it
    
    # _ is the position of index but here it is ignored
    #it give each row in series
    for _, row in dataFile.iterrows(): 
        
        #stored the correct option
        correct = str(row['correct_option']).strip().upper()
        
        #checking validity
        if correct not in ['A' , 'B' , 'C' , 'D']:
            raise ValueError(f"Invalid correct_option : {row['correct_option']}")
        

        #creating question object
        
        question = Question(
            exam = exam,
            question_text = row['question_text'],
            option_a = row['option_a'],
            option_b = row['option_b'],
            option_c = row['option_c'],
            option_d = row['option_d'],
            correct_option = correct,
            marks = (int(row.get('marks' , 1))), # if no marks feild is present the default value will be 1
        )
        
        questions.append(question)#adding new question after each iteration
        
    Question.objects.bulk_create(questions) #creating a bulk of questions in "Questions table"
    
    return len(questions) #returns the number of questions uploaded via excel