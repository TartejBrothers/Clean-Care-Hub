# Import necessary modules from Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .form import RegisterCustomerForm


User = get_user_model()


# View for customer registration
def register_customer(request):
    if request.method == "POST":
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            # Save the form data, set custom user role, and redirect to login
            user_instance = form.save(commit=False)
            user_instance.username = user_instance.email
            user_instance.save()
            messages.success(request, "Account created. Please log in")
            return redirect("login")
        else:
            # Display warning message for form errors and redirect to registration page
            messages.warning(request, "Something went wrong. Please check form errors")
            return redirect("register-customer")
    else:
        # Display registration form for GET requests
        form = RegisterCustomerForm()
        context = {"form": form}
        return render(request, "accounts/register_customer.html", context)


# View for user login
def login_user(request):
    if request.method == 'POST':
        # Authenticate user and redirect to dashboard if successful
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        else:
            # Display warning message for login failure and redirect to login page
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('login')
    else:
        # Display login form for GET requests
        return render(request, 'accounts/login.html')


# View for user logout
def logout_user(request):
    # Logout the user, display success message, and redirect to login page
    logout(request)
    messages.success(request, "Active session ended. Log in to continue")
    return redirect("login")


# Additional comments for planned features (change password, update profile) can be added here
def home(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    else:
        return redirect('login')
