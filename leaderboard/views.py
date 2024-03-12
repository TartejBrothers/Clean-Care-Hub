# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Leaderboard, Badge, Achievement

@login_required
def leaderboard_view(request):
    leaderboard = Leaderboard.objects.order_by('-points')[:10]  # Get top 10 users based on points
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard})
@login_required
def badges_view(request):
    badges = Badge.objects.all()
    return render(request, 'badges.html', {'badges': badges})
