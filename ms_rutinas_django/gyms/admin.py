from django.contrib import admin
from .models import Athlete, Exercise, Routine, RoutineExercise, WorkoutLog

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gym_id', 'weight', 'height')
    list_filter = ('gym_id',)
    search_fields = ('first_name', 'last_name')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym_id')
    list_filter = ('gym_id',)

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym_id')
    list_filter = ('gym_id',)

@admin.register(RoutineExercise)
class RoutineExerciseAdmin(admin.ModelAdmin):
    list_display = ('routine', 'exercise', 'sets', 'reps')

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'routine', 'date_completed')
    list_filter = ('date_completed',)