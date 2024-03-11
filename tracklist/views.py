from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Tracklist
from django.http import JsonResponse
from django.contrib import messages

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
    return render(request, "tracklist.html", {"form": form})


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
            task.delete()
            messages.success(request, "Great work done")
    return redirect("assigned_tasks")


def success_page(request):
    return render(request, "success.html")
