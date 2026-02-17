from .models import StudyPlan
from .forms import StudyPlanForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def create_plan(request):
    if request.method == "POST":
        form = StudyPlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('accounts:dashboard')
    else:
        form = StudyPlanForm()

    return render(request, 'create_plan.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'home.html')

@login_required
def settings_view(request):
    return render(request, 'settings.html')

@login_required
def dashboard(request):
    plans = StudyPlan.objects.filter(user=request.user).order_by('-created_at')
    plans_count = plans.count()

    return render(request, 'dashboard.html', {
        'plans': plans,
        'plans_count': plans_count
    })

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
        print("USER CREATED")
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


from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def account_settings(request):
    return render(request, 'account_settings.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


