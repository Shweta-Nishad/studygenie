from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.account_settings, name='account_settings'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-plan/', views.create_plan, name='create_plan'),
    path('plan/<int:plan_id>/', views.view_plan, name='view_plan'),
    path('quiz/generate/<int:plan_id>/', views.generate_quiz, name='generate_quiz'),
    path('quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),

]
