from rest_framework import generics, serializers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import logging
import datetime
from .models import Athlete, Exercise, Routine, RoutineExercise, WorkoutLog
from .serializers import (
    AthleteSerializer, 
    ExerciseSerializer, RoutineSerializer, 
    RoutineExerciseSerializer, WorkoutLogSerializer
)
from .services import publicar_evento_kafka

logger = logging.getLogger('calisaas_logger')

def get_gym_id_from_token(request):
    """
    Extrae el gym_id del token JWT.
    Preparado para cambiar a 'resource_access' u otra estructura si el profesor lo requiere luego.
    """
    if hasattr(request, 'auth') and request.auth:
        # Si luego viene anidado: return request.auth.get('resource_access', {}).get('calisaas', {}).get('gym_id')
        return request.auth.get('gym_id')
    return None

class GymIsolationMixin:
    """
    Mixin para garantizar que todas las consultas se filtren automáticamente
    por el gym_id contenido en el token JWT.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        gym_id = get_gym_id_from_token(self.request)
        if gym_id:
            return qs.filter(gym_id=gym_id)
        return qs.none()

# --- ATHLETE VIEWS ---
class AthleteListCreate(GymIsolationMixin, generics.ListCreateAPIView):
    serializer_class = AthleteSerializer
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return super().get_queryset()

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        logger.info(f"El usuario {request.user.username} consultó la lista de Atletas (Caché por 15 min).")
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        gym_id = get_gym_id_from_token(self.request)
        if not gym_id:
            raise serializers.ValidationError({"detail": "Falta gym_id en el token JWT."})
        
        athlete = serializer.save(gym_id=gym_id)
        
        publicar_evento_kafka('athlete_events', {
            'event_type': 'ATHLETE_CREATED',
            'athlete_id': athlete.id,
            'gym_id': gym_id,
            'first_name': athlete.first_name,
            'last_name': athlete.last_name
        })

class AthleteRetrieveUpdateDestroy(GymIsolationMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AthleteSerializer
    def get_queryset(self):
        return super().get_queryset()

# --- EXERCISE VIEWS ---
class ExerciseListCreate(GymIsolationMixin, generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer
    search_fields = ['name']

    def get_queryset(self):
        return super().get_queryset()

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        logger.info(f"El usuario {request.user.username} consultó el catálogo de Ejercicios (Caché).")
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        gym_id = get_gym_id_from_token(self.request)
        if not gym_id:
            raise serializers.ValidationError({"detail": "Falta gym_id en el token JWT."})
        serializer.save(gym_id=gym_id)

class ExerciseRetrieveUpdateDestroy(GymIsolationMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    def get_queryset(self):
        return super().get_queryset()

# --- ROUTINE VIEWS ---
class RoutineListCreate(GymIsolationMixin, generics.ListCreateAPIView):
    serializer_class = RoutineSerializer
    search_fields = ['name']

    def get_queryset(self):
        return super().get_queryset()

    def perform_create(self, serializer):
        gym_id = get_gym_id_from_token(self.request)
        if not gym_id:
            raise serializers.ValidationError({"detail": "Falta gym_id en el token JWT."})
            
        routine = serializer.save(gym_id=gym_id)
        
        publicar_evento_kafka('gym_updates', {
            'event_type': 'ROUTINE_CREATED',
            'routine_id': routine.id,
            'routine_name': routine.name,
            'gym_id': gym_id
        })

class RoutineRetrieveUpdateDestroy(GymIsolationMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineSerializer
    def get_queryset(self):
        return super().get_queryset()

# --- ROUTINE EXERCISE VIEWS ---
class RoutineExerciseListCreate(GymIsolationMixin, generics.ListCreateAPIView):
    serializer_class = RoutineExerciseSerializer
    
    def get_queryset(self):
        return super().get_queryset()

    def perform_create(self, serializer):
        gym_id = get_gym_id_from_token(self.request)
        if not gym_id:
            raise serializers.ValidationError({"detail": "Falta gym_id en el token JWT."})
        serializer.save(gym_id=gym_id)

class RoutineExerciseRetrieveUpdateDestroy(GymIsolationMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineExerciseSerializer
    def get_queryset(self):
        return super().get_queryset()

# --- WORKOUT LOG VIEWS ---
class WorkoutLogListCreate(GymIsolationMixin, generics.ListCreateAPIView):
    serializer_class = WorkoutLogSerializer
    search_fields = ['athlete__first_name', 'athlete__last_name', 'notes']

    def get_queryset(self):
        return super().get_queryset()

    def perform_create(self, serializer):
        gym_id = get_gym_id_from_token(self.request)
        if not gym_id:
            raise serializers.ValidationError({"detail": "Falta gym_id en el token JWT."})
            
        workout_log = serializer.save(gym_id=gym_id)
        
        publicar_evento_kafka('workout_metrics', {
            'event_type': 'WORKOUT_LOGGED',
            'log_id': workout_log.id,
            'athlete_id': workout_log.athlete.id if hasattr(workout_log, 'athlete') else None,
            'duration_minutes': workout_log.duration_minutes if hasattr(workout_log, 'duration_minutes') else 0,
            'gym_id': gym_id
        })

class WorkoutLogRetrieveUpdateDestroy(GymIsolationMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutLogSerializer
    def get_queryset(self):
        return super().get_queryset()