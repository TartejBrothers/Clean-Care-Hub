from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model

# Create your views here.

from django.shortcuts import render
from .forms import TracklistForm


def tracklist_form(request):
    if request.method == "POST":
        form = TracklistForm(request.POST)
        if form.is_valid():
            # Process the form data if it's valid
            form.save()
            # Redirect to a success page or render a success message
    else:
        form = TracklistForm()
    return render(request, "tracklist.html", {"form": form})
