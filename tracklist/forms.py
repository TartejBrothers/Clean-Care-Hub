from django import forms
from .models import Tracklist
import datetime


class TracklistForm(forms.ModelForm):
    class Meta:
        model = Tracklist
        fields = ["email", "description", "deadline"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control gray-bg white-text",
                    "style": "padding: 10px;",
                    "placeholder": "Enter your email",
                    "autocomplete": "off",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control gray-bg white-text",
                    "style": "padding: 10px;",
                    "placeholder": "Enter description",
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control gray-bg white-text",
                    "style": "padding: 10px;",
                    "min": str(datetime.date.today()),
                }
            )
        }
