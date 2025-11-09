# 💪 FitFrenzy — Your Personal Fitness & Health Tracker

🚀 **FitFrenzy** is a full-featured fitness and health tracking web application built using **Django**.  
It empowers users to monitor their workouts, diet, progress, and BMI — all in one clean dashboard.

---

## 🧩 Features

### 👤 User & Admin Management
- Secure login, registration, and authentication.
- Separate dashboards for **Users** and **Admins**.
- Profile updates with automatic **daily weight logging**.

### 🏋️ Workout Tracking
- Add, edit, or delete workout logs.
- **Workout suggestions API** integrated (ExerciseDB).
- Displays exercise details and (optionally) GIF animations.

### 🍎 Diet Logging
- Track daily meals with calorie information.
- View complete diet history anytime.

### 📈 Progress Tracking
- Monitor BMI, calories, and workout statistics.
- Visual graphs for weight and calorie changes.

### 🤖 Chatbot (Future Scope)
- AI-powered assistant for fitness queries and motivation.

### 💬 Recommendations
- Smart health, nutrition, and lifestyle advice.
- Links to trusted fitness resources.

---

## 🧠 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite (default) |
| **APIs** | ExerciseDB (via RapidAPI) |
| **Version Control** | Git & GitHub |

---

## ⚙️ Installation & Setup

### 1. Clone the repo  
```bash
git clone https://github.com/UjasBanke/Quiz_app.git
cd Quiz_app
```
### 2. Set up virtual environment & install dependencies  
```bash
# Create virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux / macOS
source venv/bin/activate

# On Windows (Command Prompt)
venv\Scripts\activate

# On Windows (PowerShell)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```
### 3. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Start the server
```bash
python manage.py runserver
```
### 6. Visit the site
```bash
http://127.0.0.1:8000/
```



### 🌐 API Integration

FitFrenzy uses the ExerciseDB API to provide workout suggestions:

Fetches exercises based on selected body part.

Displays name, equipment, and (optional) GIF preview.

API Source: ExerciseDB on RapidAPI


### 🎯 Future Enhancements

Mobile app integration.

Personalized diet & workout recommendations via AI.

Voice-enabled chatbot for instant guidance.

Community workout challenges.



<img width="1901" height="907" alt="image" src="https://github.com/user-attachments/assets/0cc623d5-7aac-4b84-ae52-738303dfba5a" />

