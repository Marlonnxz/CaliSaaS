from django.contrib import admin
from .models import Gym, Athlete, Exercise, Routine, RoutineExercise, WorkoutLog

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    # Cambiamos 'owner_email' por 'owner'
    list_display = ('name', 'slug', 'owner', 'created_at') 
    # También lo cambiamos en el buscador
    search_fields = ('name', 'owner__username') # Usamos __username para buscar por el nombre del usuario
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gym', 'weight', 'height')
    list_filter = ('gym',)
    search_fields = ('first_name', 'last_name')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym')
    list_filter = ('gym',)

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym')
    list_filter = ('gym',)

@admin.register(RoutineExercise)
class RoutineExerciseAdmin(admin.ModelAdmin):
    list_display = ('routine', 'exercise', 'sets', 'reps')

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'routine', 'date_completed')
    list_filter = ('date_completed',)