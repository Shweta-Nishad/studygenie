from django.db import models
from django.contrib.auth.models import User

class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    syllabus = models.TextField()
    current_grade = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    syllabus_pdf = models.FileField(upload_to='syllabus_pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
