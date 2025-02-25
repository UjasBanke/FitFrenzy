from django.contrib import admin
from django.urls import path
from main_app.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Add this line to load the homepage
]
