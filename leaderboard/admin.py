# admin.py
from django.contrib import admin
from .models import Leaderboard, Badge, Achievement

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__username',)
    list_filter = ('points',)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'date_achieved')
    search_fields = ('user__username', 'badge__name')
    list_filter = ('badge', 'date_achieved')

