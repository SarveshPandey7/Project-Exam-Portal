from django import forms

class QuestionUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload Excel File",
        help_text="Upload .xlsx file with MCQ questions"
    )
    