from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Get the User model dynamically to support custom user models
User = get_user_model()

# Create a custom form for customer registration, inheriting from UserCreationForm
class RegisterCustomerForm(UserCreationForm):
    class Meta:
        # Specify the model for which the form is created (custom User model)
        model = User

        # Specify the fields to be included in the form
        fields = ['email', 'password1', 'password2']