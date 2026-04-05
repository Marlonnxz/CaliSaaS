from django.urls import path
from .views import GymListCreate

urlpatterns = [
    path('gyms/', GymListCreate.as_view(), name='gym-list'),
]

