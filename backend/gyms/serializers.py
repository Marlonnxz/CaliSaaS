from rest_framework import serializers
from .models import Gym, Athlete

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'