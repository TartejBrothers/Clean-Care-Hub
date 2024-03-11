# Import necessary modules from Django
from django.urls import path
from . import views

# URL patterns for user authentication and registration
urlpatterns = [
    # Path for registering a customer
    path("signup/", views.register_customer, name="register-customer"),
    # Path for user login
    path("login/", views.login_user, name="login"),
    # Path for user logout
    path("logout/", views.logout_user, name="logout"),
    path("",views.home , name="home")
]
