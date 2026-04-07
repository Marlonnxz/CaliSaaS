from django.urls import path
from .views import (
    GymListCreate, GymRetrieveUpdateDestroy,
    AthleteListCreate, AthleteRetrieveUpdateDestroy,
    ExerciseListCreate, ExerciseRetrieveUpdateDestroy,
    RoutineListCreate, RoutineRetrieveUpdateDestroy,
    RoutineExerciseListCreate, RoutineExerciseRetrieveUpdateDestroy,
    WorkoutLogListCreate, WorkoutLogRetrieveUpdateDestroy
)

urlpatterns = [
    path('gyms/', GymListCreate.as_view(), name='gym-list'),
    path('gyms/<int:pk>/', GymRetrieveUpdateDestroy.as_view(), name='gym-detail'),
    
    path('athletes/', AthleteListCreate.as_view(), name='athlete-list'),
    path('athletes/<int:pk>/', AthleteRetrieveUpdateDestroy.as_view(), name='athlete-detail'),
    
    path('exercises/', ExerciseListCreate.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', ExerciseRetrieveUpdateDestroy.as_view(), name='exercise-detail'),
    
    path('routines/', RoutineListCreate.as_view(), name='routine-list'),
    path('routines/<int:pk>/', RoutineRetrieveUpdateDestroy.as_view(), name='routine-detail'),
    
    path('routine-exercises/', RoutineExerciseListCreate.as_view(), name='routine-exercise-list'),
    path('routine-exercises/<int:pk>/', RoutineExerciseRetrieveUpdateDestroy.as_view(), name='routine-exercise-detail'),
    
    path('workout-logs/', WorkoutLogListCreate.as_view(), name='workout-log-list'),
    path('workout-logs/<int:pk>/', WorkoutLogRetrieveUpdateDestroy.as_view(), name='workout-log-detail'),
]