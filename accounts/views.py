from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from math import ceil
from PyPDF2 import PdfReader
from datetime import date, timedelta
from .models import StudyPlan
import re
from .models import Quiz, Question
import random
from .models import UserQuizAttempt


# ==============================
# HOME
# ==============================

def home(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'home.html')


# ==============================
# CREATE PLAN
# ==============================

@login_required
def create_plan(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        subject = request.POST.get("subject")
        current_grade = request.POST.get("current_grade")
        target_grade = request.POST.get("target_grade")
        duration_weeks = request.POST.get("duration_weeks")
        daily_hours = request.POST.get("study_hours_per_day")
        syllabus_text = request.POST.get("syllabus")
        pdf_file = request.FILES.get("syllabus_pdf")

        if not duration_weeks or not daily_hours:
            return render(request, "create_plan.html", {
                "error": "Please fill all required fields."
            })

        duration_weeks = int(duration_weeks)
        daily_hours = int(daily_hours)

        # Extract text from PDF
        if pdf_file:
            reader = PdfReader(pdf_file)
            syllabus_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    syllabus_text += text + "\n"

        # Convert syllabus into topics

        if syllabus_text:
            raw_lines = syllabus_text.split("\n")

            topics = []

            for line in raw_lines:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip unit/module headings
                if re.search(r'unit\s*\d+|module\s*\d+', line.lower()):
                    continue

                # Skip lines that are mostly numbers or page indexes
                if re.match(r'^\d+(\.\d+)*\s*$', line):
                    continue

                # Skip very short fragments
                if len(line.split()) < 3:
                    continue

                # Skip lines with too many dots (table of contents style)
                if "...." in line:
                    continue

                # Keep meaningful short headings only
                if len(line) < 80:
                    topics.append(line)               

        else:
            topics = []


        total_days = duration_weeks * 7
        topics_per_day = ceil(len(topics) / total_days) if topics else 1

        study_plan_data = []
        topic_index = 0

        for day in range(1, total_days + 1):
            daily_topics = topics[topic_index:topic_index + topics_per_day]
            topic_index += topics_per_day

            if not daily_topics:
                break

            study_plan_data.append({
                "day": day,
                "topics": daily_topics
            })

        # SAVE TO DATABASE
        plan = StudyPlan.objects.create(
            user=request.user,
            title=course_name,
            subject=subject,
            current_grade=current_grade,
            start_date=date.today(),
            end_date=date.today() + timedelta(weeks=duration_weeks),
            syllabus=syllabus_text,
            syllabus_pdf=pdf_file,
            generated_plan=study_plan_data  #Store generated plan in JSONField
        )

        # plan.generated_plan = study_plan_data
        # plan.save()

        context = {
            "course_name": course_name,
            "subject": subject,
            "study_plan": study_plan_data,
            "daily_hours": daily_hours
        }

        return render(request, "plan_result.html", context)

    return render(request, "create_plan.html")

#==============================
# GENERATE QUIZ
#==============================
@login_required
def generate_quiz(request, plan_id):
    plan = StudyPlan.objects.get(id=plan_id, user=request.user)

    if not plan.generated_plan:
        return redirect("accounts:dashboard")

    topics = plan.generated_plan[0].get("topics", [])

    # Limit topic length
    clean_topics = []
    for t in topics:
        if len(t) < 60:
            clean_topics.append(t)

    topics = clean_topics[:5]


    quiz = Quiz.objects.create(
        study_plan=plan,
        topic=", ".join(topics)
    )

    # Simple Demo Questions (Replace later with AI)
    for topic in topics[:3]:  # 3 questions
        Question.objects.create(
            quiz=quiz,
            question_text=f"Which of the following best describes '{topic}'?",
            option_a=f"A basic explanation of {topic}",
            option_b=f"An advanced theory related to {topic}",
            option_c=f"A practical application of {topic}",
            option_d=f"An unrelated concept",
            correct_answer="A"
        )


        return redirect("accounts:start_quiz", quiz.id)

#==============================
# START QUIZ
#==============================
@login_required
def start_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question_set.all()

    return render(request, "quiz.html", {
        "quiz": quiz,
        "questions": questions
    })

from .models import UserQuizAttempt

# ==============================
# SUBMIT QUIZ SCORE
# ==============================
@login_required
def submit_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question_set.all()

    score = 0

    for question in questions:
        selected = request.POST.get(f"question_{question.id}")
        if selected == question.correct_answer:
            score += 1

    UserQuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score
    )

    return render(request, "quiz_result.html", {
        "quiz": quiz,
        "score": score,
        "total": questions.count()
    })

# ==============================
# DASHBOARD
# ==============================

@login_required
def dashboard(request):
    plans = StudyPlan.objects.filter(user=request.user).order_by('-created_at')
    plans_count = plans.count()

    return render(request, 'dashboard.html', {
        'plans': plans,
        'plans_count': plans_count
    })

@login_required
def view_plan(request, plan_id):
    plan = StudyPlan.objects.get(id=plan_id, user=request.user)

    return render(request, "plan_result.html", {
        "course_name": plan.title,
        "subject": plan.subject,
        "study_plan": [],  # agar JSONField me store nahi kiya hai to temporarily empty
        "daily_hours": plan.study_hours_per_day if hasattr(plan, 'study_hours_per_day') else 2
    })

# ==============================
# AUTH
# ==============================

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("accounts:register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect("accounts:login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("accounts:login")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# ==============================
# PROFILE & SETTINGS
# ==============================

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def account_settings(request):
    return render(request, 'account_settings.html')
