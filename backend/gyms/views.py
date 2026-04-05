from rest_framework import generics
from .models import Gym
from .serializers import GymSerializer

class GymListCreate(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer