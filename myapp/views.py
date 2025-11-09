from datetime import date
import json
import requests
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import RegisterForm, ProfileForm
from .models import Profile, Diet, WeightLog, Workout
# -------------------- HOME --------------------
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home_logged.html')
    return render(request, 'home.html')


# -------------------- AUTHENTICATION --------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username').strip()
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()

            profile = user.profile
            profile.dob = profile_form.cleaned_data.get('dob')
            profile.height_cm = profile_form.cleaned_data.get('height_cm')
            profile.weight_kg = profile_form.cleaned_data.get('weight_kg')
            profile.save()

            messages.success(request, "Account created successfully! Please log in to continue.")
            return redirect('login')  

    else:
        form = RegisterForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})





def login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username_input, password=password)

        if user is None:
            from django.contrib.auth.models import User
            try:
                user_obj = User.objects.get(username__iexact=username_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')





def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('home')


# -------------------- PROFILE --------------------
@login_required
def profile_view(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            
            # Also log the new weight if it was provided
            weight = form.cleaned_data.get('weight_kg')
            if weight:
                # Use update_or_create to prevent duplicate weight logs for the same day
                WeightLog.objects.update_or_create(
                    user=request.user, 
                    date=date.today(),
                    defaults={'weight_kg': weight}
                )
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})


# -------------------- DASHBOARD --------------------
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# -------------------- BMI --------------------
def bmi_view(request):
    bmi = category = None
    if request.method == 'POST':
        try:
            height = float(request.POST.get('height'))
            weight = float(request.POST.get('weight'))
            bmi = round(weight / ((height / 100) ** 2), 2)

            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
        except (TypeError, ValueError):
            messages.error(request, "Please enter valid height and weight.")
    return render(request, 'bmi.html', {'bmi': bmi, 'category': category})


# -------------------- WORKOUT --------------------
@login_required
def workout_log_view(request):
    if request.method == 'POST':
        workout = request.POST.get('workout')
        duration = request.POST.get('duration')
        calories = request.POST.get('calories')

        if all([workout, duration, calories]):
            Workout.objects.create(
                user=request.user,
                workout=workout,
                duration=int(duration),
                calories=int(calories)
            )

    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workout_log.html', {'workouts': workouts})


@login_required
def workout_history_view(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workout_history.html', {'workouts': workouts})


@login_required
def edit_workout_view(request, workout_id):
    workout = Workout.objects.filter(id=workout_id, user=request.user).first()
    if not workout:
        return redirect('workout_history')

    if request.method == 'POST':
        workout.workout = request.POST.get('workout')
        workout.duration = request.POST.get('duration')
        workout.calories = request.POST.get('calories')
        workout.date = request.POST.get('date')
        workout.save()
        return redirect('workout_history')

    return render(request, 'edit_workout.html', {'workout': workout})


@login_required
def delete_workout_view(request, workout_id):
    workout = Workout.objects.filter(id=workout_id, user=request.user).first()
    if workout:
        workout.delete()
    return redirect('workout_history')


# -------------------- DIET --------------------
@login_required
def diet_log_view(request):
    if request.method == 'POST':
        meal = request.POST.get('meal')
        food_item = request.POST.get('food_item')
        calories = request.POST.get('calories')
        Diet.objects.create(user=request.user, meal=meal, food_item=food_item, calories=calories)
        return redirect('diet_history')
    return render(request, 'diet_log.html')


@login_required
def diet_history_view(request):
    diets = Diet.objects.filter(user=request.user).order_by('-date')
    return render(request, 'diet_history.html', {'diets': diets})


@login_required
def edit_diet_view(request, diet_id):
    diet = Diet.objects.filter(id=diet_id, user=request.user).first()
    if not diet:
        return redirect('diet_history')

    if request.method == 'POST':
        diet.meal = request.POST.get('meal')
        diet.food_item = request.POST.get('food_item')
        diet.calories = request.POST.get('calories')
        diet.date = request.POST.get('date')
        diet.save()
        return redirect('diet_history')

    return render(request, 'edit_diet.html', {'diet': diet})


@login_required
def delete_diet_view(request, diet_id):
    diet = Diet.objects.filter(id=diet_id, user=request.user).first()
    if diet:
        diet.delete()
    return redirect('diet_history')


# -------------------- RECOMMENDATIONS --------------------
def recommendations_view(request):
    return render(request, 'recommendations.html')


# -------------------- PROGRESS --------------------
@login_required
def progress_view(request):
    user = request.user

    # Workout and weight data
    workouts = Workout.objects.filter(user=user).order_by('date')
    weights = WeightLog.objects.filter(user=user).order_by('date')

    # Extract data for visualization
    calorie_labels = [w.date.strftime('%b %d') for w in workouts]
    calorie_values = [w.calories for w in workouts]
    weight_labels = [w.date.strftime('%b %d') for w in weights]
    weight_values = [w.weight_kg for w in weights]

    # Progress summaries
    workouts_month = workouts.filter(date__month=date.today().month).count()
    total_calories = workouts.aggregate(Sum('calories'))['calories__sum'] or 0

    profile = user.profile
    h = (profile.height_cm or 0) / 100
    cw = float(profile.weight_kg or 0)
    current_bmi = round(cw / (h * h), 1) if h else 0

    bmi_status = (
        "Underweight" if current_bmi < 18.5 else
        "Healthy" if current_bmi < 25 else
        "Overweight" if current_bmi < 30 else
        "Obese"
    )

    weight_change = round(weight_values[-1] - weight_values[0], 1) if len(weight_values) >= 2 else 0

    context = {
        'calorie_labels': json.dumps(calorie_labels),
        'calorie_values': json.dumps(calorie_values),
        'weight_labels': json.dumps(weight_labels),
        'weight_values': json.dumps(weight_values),
        'workouts_month': workouts_month,
        'total_calories': total_calories,
        'current_bmi': current_bmi,
        'bmi_status': bmi_status,
        'weight_change': weight_change,
    }
    return render(request, 'progress.html', context)




#API
import requests
from django.shortcuts import render

def workout_suggestions_view(request):
    """
    Fetch workout suggestions from ExerciseDB API based on selected body part.
    """
    BASE_URL = "https://exercisedb.p.rapidapi.com"
    HEADERS = {
        "x-rapidapi-host": "exercisedb.p.rapidapi.com",
        "x-rapidapi-key": "3fa3810289msh7dca1cbc278752ap140bbbjsn964b85c85d5c"
    }

    exercises = []
    error_message = None
    body_parts = []

    try:
        list_response = requests.get(f"{BASE_URL}/exercises/bodyPartList", headers=HEADERS)
        if list_response.status_code == 200:
            body_parts = list_response.json()
            print("✅ Body Parts List:", body_parts)
        else:
            error_message = "Unable to fetch body parts list."
    except Exception as e:
        error_message = f"API Error (List): {e}"

 
    if request.method == "POST":
        selected_part = request.POST.get("body_part")

        if selected_part:
            try:
                response = requests.get(
                    f"{BASE_URL}/exercises/bodyPart/{selected_part.lower()}",
                    headers=HEADERS
                )

                if response.status_code == 200:
                    exercises = response.json()
                    print(f"✅ First Exercise Sample: {exercises[0] if exercises else 'No exercises found'}")

                  
                    for e in exercises:
                        gif_url = e.get("gifUrl")

                        if not gif_url or "undefined" in gif_url or "null" in gif_url:
                            e["gifUrl"] = "https://via.placeholder.com/200x200.png?text=No+Image"
                        else:
                           
                            e["gifUrl"] = gif_url.replace("http://", "https://")
                 
                  

                else:
                    error_message = f"Failed to fetch exercises (HTTP {response.status_code})"
            except Exception as e:
                error_message = f"API Error (Exercises): {e}"


    return render(request, "workout_suggestions.html", {
        "body_parts": body_parts,
        "exercises": exercises,
        "error_message": error_message,
    })
