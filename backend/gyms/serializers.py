from rest_framework import serializers
from .models import Gym, Athlete, Exercise, Routine, RoutineExercise, WorkoutLog

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'
        read_only_fields = ['owner'] 

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class RoutineExerciseSerializer(serializers.ModelSerializer):
    # Opcional: mostrar detalles del ejercicio en lectura
    exercise_name = serializers.ReadOnlyField(source='exercise.name')

    class Meta:
        model = RoutineExercise
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    routine_exercises = RoutineExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = '__all__'

class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = '__all__'