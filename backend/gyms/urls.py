from django.urls import path
from .views import GymListCreate, AthleteListCreate 

urlpatterns = [
    path('gyms/', GymListCreate.as_view(), name='gym-list'),
    path('athletes/', AthleteListCreate.as_view(), name='athlete-list'), 
]