from rest_framework import serializers
from .models import Gym, Athlete

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'
        read_only_fields = ['owner'] 

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'