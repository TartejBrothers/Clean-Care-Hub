# Import necessary modules from Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Import the User model from the current application
from .models import User


# Register the User model with the custom admin class
admin.site.register(User)