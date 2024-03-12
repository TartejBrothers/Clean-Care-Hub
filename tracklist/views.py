from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Tracklist
from django.http import JsonResponse
from django.contrib import messages
from .forms import TracklistForm
from django.contrib import messages
from leaderboard.models import Leaderboard, Achievement, Badge

# Create your views here.

from django.shortcuts import render
from .forms import TracklistForm


@login_required
def tracklist_form(request):
    if request.method == "POST":
        form = TracklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("../success_page")
    else:
        form = TracklistForm()

    if request.user.is_superuser:
        return render(request, "tracklist.html", {"form": form})
    else:
        return render(request, "adminaccess.html")


@login_required
def view_assigned_tasks(request):
    user_email = request.user.email
    assigned_tasks = Tracklist.objects.filter(email=user_email)
    return render(request, "assigned_tasks.html", {"assigned_tasks": assigned_tasks})


def update_task_status(request, task_id):
    if request.method == "POST":
        task = Tracklist.objects.get(pk=task_id)
        status = request.POST.get("status")
        if status == "yes":
            # Increase points for the user
            user = request.user
            points_earned = 5  # Adjust points based on your criteria
            leaderboard, created = Leaderboard.objects.get_or_create(user=user)
            leaderboard.points += points_earned
            leaderboard.save()

            # Check if the user has earned any badges
            if leaderboard.points >= 50:
                badge, created = Badge.objects.get_or_create(name="Sanitation Master", description="Awarded for completing 5 successful sanitation checks.")
                Achievement.objects.create(user=user, badge=badge)
            
            task.delete()
            messages.success(request, "Great work done")
    return redirect("assigned_tasks")


def success_page(request):
    return render(request, "success.html")
