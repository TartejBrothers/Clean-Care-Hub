from django import forms
from .models import Tracklist

class TracklistForm(forms.ModelForm):
    class Meta:
        model = Tracklist
        fields = ["email", "description", "deadline"]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
