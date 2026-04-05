from django.contrib import admin
from .models import Gym, Athlete

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner_email', 'created_at')
    search_fields = ('name', 'owner_email')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gym', 'weight', 'height')
    list_filter = ('gym',)
    search_fields = ('first_name', 'last_name')