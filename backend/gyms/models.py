from django.db import models
from django.conf import settings
from core.middleware import get_current_request

class TenantManager(models.Manager):
    """
    Manager que filtra dinámicamente los registros de acuerdo al 
    usuario autenticado que hace la solicitud.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        request = get_current_request()
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # Los Súper Administradores pueden ver absolutamente todos los registros
            if request.user.is_superuser:
                return qs
            # Para Gym filtramos directamente el owner
            if self.model.__name__ == 'Gym':
                return qs.filter(owner=request.user)
            # Para todos los modelos hijos, filtramos su gimnasio padre
            elif hasattr(self.model, 'gym'):
                return qs.filter(gym__owner=request.user)
        return qs

class Gym(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_gyms'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = TenantManager()

    def __str__(self):
        return self.name



class Athlete(models.Model):
    # EL DISCRIMINADOR: Esta llave foránea es la frontera que separa 
    # los atletas de un gimnasio (Tenant A) de los de otro (Tenant B).
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='athletes')
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    weight = models.FloatField(help_text="Peso en kg")
    height = models.FloatField(help_text="Altura en metros")
    
    objects = TenantManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.gym.name}"

class Exercise(models.Model):
    # Tenant aislado: El dueño crea sus propios ejercicios en su gimnasio
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='exercises')
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = TenantManager()

    def __str__(self):
        return self.name

class Routine(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='routines')
    
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = TenantManager()

    def __str__(self):
        return self.name

class RoutineExercise(models.Model):
    # Este modelo vincula rutinas con ejercicios (Many-to-Many enriquecido)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='routine_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    # Redundancia explícita de tenant para que el TenantManager lo filtre directamente:
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)
    rest_seconds = models.PositiveIntegerField(default=60)
    
    objects = TenantManager()

    def __str__(self):
        return f"{self.routine.name} - {self.exercise.name} ({self.sets}x{self.reps})"

class WorkoutLog(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='workout_logs')
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, blank=True)
    
    date_completed = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    objects = TenantManager()

    def __str__(self):
        return f"Log {self.athlete.first_name} - {self.date_completed.strftime('%Y-%m-%d')}"