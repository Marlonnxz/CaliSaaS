from django.db import models
from django.conf import settings

class Athlete(models.Model):
    gym_id = models.CharField(max_length=255, help_text="ID del gimnasio inyectado desde el token JWT")
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    weight = models.FloatField(help_text="Peso en kg")
    height = models.FloatField(help_text="Altura en metros")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Exercise(models.Model):
    gym_id = models.CharField(max_length=255, help_text="ID del gimnasio inyectado desde el token JWT")
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Routine(models.Model):
    gym_id = models.CharField(max_length=255, help_text="ID del gimnasio inyectado desde el token JWT")
    
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RoutineExercise(models.Model):
    gym_id = models.CharField(max_length=255, help_text="ID del gimnasio inyectado desde el token JWT")
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='routine_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)
    rest_seconds = models.PositiveIntegerField(default=60)

    def __str__(self):
        return f"{self.routine.name} - {self.exercise.name} ({self.sets}x{self.reps})"

class WorkoutLog(models.Model):
    gym_id = models.CharField(max_length=255, help_text="ID del gimnasio inyectado desde el token JWT")
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='workout_logs')
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, blank=True)
    
    date_completed = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log {self.athlete.first_name} - {self.date_completed.strftime('%Y-%m-%d')}"