# 📘 StudyGenie

StudyGenie is a smart AI-powered study planner and quiz generator built using Django.  
It helps students create structured study plans from syllabus PDFs and automatically generates practice quizzes to test understanding.

---

## 🚀 Features

- User Authentication (Register/Login/Logout)
- Create Personalized Study Plans
- Upload Syllabus (PDF Supported)
- Auto Topic Extraction
- Automatic Quiz Generation
- Multiple Choice Questions (MCQs)
- Score Calculation
- Quiz Result Page
- Dashboard with Recent Plans

---

## 🛠️ Tech Stack

- **Backend:** Django 6
- **Frontend:** HTML, CSS (Glassmorphism UI)
- **Database:** SQLite (default)
- **PDF Parsing:** PyPDF2
- **Authentication:** Django Auth System

---

## 📂 Project Structure

StudyGenie/
│
├── accounts/ # Main App
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│
├── templates/
│ ├── base.html
│ ├── dashboard.html
│ ├── quiz.html
│ ├── quiz_result.html
│
├── db.sqlite3
├── manage.py
└── README.md

---

## ⚙️ Installation & Setup

### 1️. Clone the repository
   git clone https://github.com/yourusername/studygenie.git
   cd studygenie

### 2️. Create Virtual Environment
   python -m venv venv
   venv\Scripts\activate   # Windows

### 3️. Install Dependencies
   pip install -r requirements.txt

### 4️. Run Migrations
   python manage.py migrate

### 5️. Start Server
   python manage.py runserver


## 🌐 Open in browser:

http://127.0.0.1:8000/

---

## 🧠 How It Works

- User uploads syllabus (PDF or text)
- System extracts structured topics
- Study plan is generated
- User can generate quizfor a plan
- MCQs are created dynamically
- User attempts quiz
- Score is calculated and stored 

---

## 📊 Future Improvements

- AI-generated intelligent MCQs
- Detailed Progress Analytics
- Daily Study Reminders
- Leaderboard System
- Deployment on Render / Railway / AWS
