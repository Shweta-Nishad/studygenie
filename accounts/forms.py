from django import forms
from .models import StudyPlan

class StudyPlanForm(forms.ModelForm):
    class Meta:
        model = StudyPlan
        fields = [
            'title',
            'subject',
            'syllabus',
            'current_grade',
            'start_date',
            'end_date',
            'syllabus_pdf'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
