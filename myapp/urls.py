from django.urls import path
from . import views
    


urlpatterns = [
    # Core pages
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User profile and dashboard
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Fitness tools
    path('bmi/', views.bmi_view, name='bmi'),
    path('progress/', views.progress_view, name='progress'),
    path('recommendations/', views.recommendations_view, name='recommendations'),

    # Workout management
    path('workout/', views.workout_log_view, name='workout'),
    path('workout/history/', views.workout_history_view, name='workout_history'),
    path('workout/edit/<int:workout_id>/', views.edit_workout_view, name='edit_workout'),
    path('workout/delete/<int:workout_id>/', views.delete_workout_view, name='delete_workout'),

    # Diet management
    path('diet/', views.diet_log_view, name='diet'),
    path('diet/history/', views.diet_history_view, name='diet_history'),
    path('diet/edit/<int:diet_id>/', views.edit_diet_view, name='edit_diet'),
    path('diet/delete/<int:diet_id>/', views.delete_diet_view, name='delete_diet'),

   #API
 
   path('workout/suggestions/', views.workout_suggestions_view, name='workout_suggestions'),





   

]
