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

    generated_plan = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz - {self.topic}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # A/B/C/D

    def __str__(self):
        return self.question_text

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

