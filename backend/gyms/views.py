from rest_framework import generics, serializers
from .models import Gym, Athlete, Exercise, Routine, RoutineExercise, WorkoutLog
from .serializers import (
    GymSerializer, AthleteSerializer, 
    ExerciseSerializer, RoutineSerializer, 
    RoutineExerciseSerializer, WorkoutLogSerializer
)
from .services import send_athlete_created_event

# --- GYM VIEWS ---
class GymListCreate(generics.ListCreateAPIView):
    serializer_class = GymSerializer
    search_fields = ['name']

    def get_queryset(self):
        return Gym.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GymRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GymSerializer
    def get_queryset(self):
        return Gym.objects.all()

# --- ATHLETE VIEWS ---
class AthleteListCreate(generics.ListCreateAPIView):
    serializer_class = AthleteSerializer
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return Athlete.objects.all()

    def perform_create(self, serializer):
        gym = serializer.validated_data.get('gym')
        if gym.owner != self.request.user:
            raise serializers.ValidationError(
                {"gym": "Acceso denegado: No puedes agregar atletas a un gimnasio que no te pertenece."}
            )
        athlete = serializer.save()
        send_athlete_created_event(athlete)

class AthleteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AthleteSerializer
    def get_queryset(self):
        return Athlete.objects.all()

# --- EXERCISE VIEWS ---
class ExerciseListCreate(generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer
    search_fields = ['name']

    def get_queryset(self):
        return Exercise.objects.all()

class ExerciseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    def get_queryset(self):
        return Exercise.objects.all()

# --- ROUTINE VIEWS ---
class RoutineListCreate(generics.ListCreateAPIView):
    serializer_class = RoutineSerializer
    search_fields = ['name']

    def get_queryset(self):
        return Routine.objects.all()

class RoutineRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineSerializer
    def get_queryset(self):
        return Routine.objects.all()

# --- ROUTINE EXERCISE VIEWS ---
class RoutineExerciseListCreate(generics.ListCreateAPIView):
    serializer_class = RoutineExerciseSerializer
    
    def get_queryset(self):
        return RoutineExercise.objects.all()

class RoutineExerciseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineExerciseSerializer
    def get_queryset(self):
        return RoutineExercise.objects.all()

# --- WORKOUT LOG VIEWS ---
class WorkoutLogListCreate(generics.ListCreateAPIView):
    serializer_class = WorkoutLogSerializer
    search_fields = ['athlete__first_name', 'athlete__last_name', 'notes']

    def get_queryset(self):
        return WorkoutLog.objects.all()

class WorkoutLogRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutLogSerializer
    def get_queryset(self):
        return WorkoutLog.objects.all()