# Import the AppConfig class from the Django apps module
from django.apps import AppConfig

# Create an AppConfig for the 'accounts' app
class AccountsConfig(AppConfig):
    # Specify the default auto field for model creation
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app to 'accounts'
    name = 'accounts'
